import os, re, json, time, argparse, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.isotonic import IsotonicRegression
from scipy.stats import spearmanr
from scipy import interpolate, optimize
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=FutureWarning)
pd.set_option("display.width", 200); pd.set_option("display.max_columns", 200)
CANDIDATE_COLS = ["zb","m","order","order_parameter","op","z_b"]

def extract_T_from_name(name: str, regex: str) -> float:
    m = re.findall(regex, name)
    if not m: raise ValueError(f"Cannot extract T by regex={regex} from {name}")
    s = str(m[-1]).strip().rstrip(".")
    return float(s)

def load_series(path: Path, require_col: str|None) -> np.ndarray|None:
    df = pd.read_csv(path)
    if require_col is not None:
        if require_col not in df.columns: return None
        x = df[require_col].to_numpy(dtype=float)
    else:
        col = None
        for c in CANDIDATE_COLS:
            if c in df.columns: col=c; break
        if col is None:
            num = df.select_dtypes(include=[np.number])
            if num.shape[1]==0: return None
            col = num.var().sort_values(ascending=False).index[0]
        x = df[col].to_numpy(dtype=float)
    x = x[np.isfinite(x)]
    return x if x.size>0 else None

def per_file_deltaF(path: Path, T: float, cstar: float, require_col: str|None):
    x = load_series(path, require_col)
    if x is None: return None
    m_mean = float(np.mean(x))
    sign_rule = np.sign(m_mean - cstar) if np.isfinite(m_mean) else 1.0
    L = np.count_nonzero(x <= cstar); R = np.count_nonzero(x > cstar); n = int(L+R)
    if n==0: return None
    eps = 0.5
    p_plus = (R+eps)/(n+2*eps); p_minus = (L+eps)/(n+2*eps)
    dF_abs = float(T*np.log(max(p_plus,p_minus)/min(p_plus,p_minus)))
    dF = float(sign_rule*dF_abs)
    se = float(1.25*T/max(np.sqrt(n),1.0))
    return {"path":str(path),"T":float(T),"n":n,"DeltaF_signed":dF,"se":se}

def aggregate_by_T(df: pd.DataFrame) -> pd.DataFrame:
    out=[]
    for T,g in df.groupby("T"):
        w = 1.0/np.maximum(g["se"].to_numpy(),1e-12)**2
        x = g["DeltaF_signed"].to_numpy()
        mu = float(np.sum(w*x)/np.sum(w))
        resid2 = np.sum(w*(x-mu)**2)/max(len(g)-1,1)
        scale = max(1.0, float(np.sqrt(resid2)))
        se_mu = float(np.sqrt(1.0/np.sum(w))*scale)
        out.append({"T":float(T),"DeltaF":mu,"SE":se_mu,"n_files":int(len(g))})
    d=pd.DataFrame(out).sort_values("T").reset_index(drop=True)
    # SEフロア：複数ファイル点のSE中央値を単独点に適用
    if (d["n_files"]>=2).any():
        se_floor = np.nanmedian(d.loc[d["n_files"]>=2,"SE"])
        d.loc[d["n_files"]==1,"SE"] = np.maximum(d.loc[d["n_files"]==1,"SE"], se_floor)
    d["CI_low"]=d["DeltaF"]-1.96*d["SE"]; d["CI_high"]=d["DeltaF"]+1.96*d["SE"]
    return d

def find_zero_linear(Tv, Fv):
    s=np.sign(Fv)
    for i in range(len(Tv)-1):
        if s[i]==0: return float(Tv[i])
        if s[i]*s[i+1]<0:
            t0,t1=Tv[i],Tv[i+1]; f0,f1=Fv[i],Fv[i+1]
            return float(t0 + (0-f0)*(t1-t0)/(f1-f0+1e-20))
    return np.nan

def isotonic_zero_auto(Ti, Fi):
    # 方向はSSEの小さい方（increasing True/False）を採用
    best=None
    for inc in (True, False):
        iso=IsotonicRegression(increasing=inc, out_of_bounds="clip")
        Fi_fit=iso.fit_transform(Ti, Fi)
        sse=float(np.sum((Fi_fit-Fi)**2))
        z=find_zero_linear(Ti, Fi_fit)
        cand=(sse, z, Fi_fit, inc)
        if (best is None) or (sse<best[0]): best=cand
    _, z, Fi_fit, inc = best
    return z, Fi_fit, inc

def reopt_cstar(paths: list[Path], regex: str, require_col: str|None, top_k:int=3):
    Ts=[]
    for p in paths:
        try: T=extract_T_from_name(p.name, regex); Ts.append((T,p))
        except: pass
    if not Ts: return 0.0
    Ts=sorted(Ts, key=lambda t:t[0])
    # 上位温度のユニークTからtop_k選抜
    uniqT=sorted({t for t,_ in Ts})[-top_k:]
    sel=[(p,T) for T,p in Ts if T in uniqT]
    xs=[]
    for p,T in sel:
        x=load_series(p, require_col)
        if x is not None: xs.append(x[::20] if x.size//20>50000 else x)
    if not xs: return 0.0
    x_all=np.concatenate(xs); lo,hi=np.percentile(x_all,[0.5,99.5])
    bins=2048; edges=np.linspace(lo,hi,bins+1)
    H=0
    for p,T in sel:
        x=load_series(p, require_col)
        if x is None: continue
        h,_=np.histogram(x,bins=edges); H=H+h
    if H.sum()==0: return 0.0
    F=np.cumsum(H)/H.sum()
    def J(c):
        pos=(c-lo)/(hi-lo)*(bins-1); idx=int(np.clip(np.round(pos),0,bins-1))
        pL=F[idx]; pR=1.0-pL
        if pL<=0 or pR<=0: return 1e12
        return (np.log(pR/pL))**2
    grid=np.linspace(lo,hi,257); vals=np.array([J(c) for c in grid])
    j=int(np.argmin(vals)); a,b=grid[max(0,j-1)], grid[min(len(grid)-1,j+1)]
    res=optimize.minimize_scalar(J,bounds=(a,b),method="bounded",options={"xatol":1e-9})
    return float(res.x)

def plot_monotone(L, T_all, F_all, T_win, F_fit, z, out_pdf, note):
    plt.figure(figsize=(6,4), dpi=150)
    plt.axhline(0, color="k", lw=1, alpha=0.6)
    plt.scatter(T_all, F_all, s=18, color="#1f77b4", label="ΔF (agg)")
    if len(T_win)>0: plt.plot(T_win, F_fit, color="#d62728", lw=2, label=note)
    if np.isfinite(z): plt.axvline(z, color="#2ca02c", lw=1.5, ls="--", label=f"T_sym≈{z:.6f}")
    else: plt.text(0.97,0.95,"T_sym = NaN (no root in window)", transform=plt.gca().transAxes, ha="right", va="top", fontsize=9, bbox=dict(boxstyle="round", fc="wheat", alpha=0.6))
    plt.xlabel("T"); plt.ylabel("ΔF (signed)"); plt.title(f"L={L}: ΔF vs T (FH policy)")
    plt.legend(loc="best", fontsize=9); plt.tight_layout(); plt.savefig(out_pdf); plt.close()

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument("--data_dir", required=True)
    ap.add_argument("--globs", required=True, help='semicolon-separated patterns')
    ap.add_argument("--regex", required=True)
    ap.add_argument("--L", required=True, type=int)
    ap.add_argument("--bundles", nargs="+", default=["Final","HighRes"])
    ap.add_argument("--exclude_substr", nargs="*", default=[])
    ap.add_argument("--require_col", default="zb")  # 強制
    ap.add_argument("--twin", nargs=2, required=True, type=float)
    ap.add_argument("--n_boot", type=int, default=200)
    # n_jobsは意図的に削除し、常に直列実行とする
    args=ap.parse_args()

    data_dir=Path(args.data_dir)
    patterns=[p for p in args.globs.split(";") if p.strip()]
    paths=[]
    for pat in patterns: paths+=list(data_dir.glob(pat.strip()))
    if not paths: raise SystemExit("No files matched.")
    # 束フィルタ
    keep=[]
    for p in paths:
        name=p.name
        if args.bundles and not any(b in name for b in args.bundles): continue
        if args.exclude_substr and any(x in name for x in args.exclude_substr): continue
        keep.append(p)
    paths=sorted(keep)
    if not paths: raise SystemExit("No files after filters.")

    # c*再最適化（高温上位K点から）
    cstar=reopt_cstar(paths, args.regex, args.require_col, top_k=4)
    print(f"[c* reopt] L={args.L}, c*={cstar:.9g}, files={len(paths)}")

    # per-file
    recs=[]
    for i,p in enumerate(paths,1):
        try: T=extract_T_from_name(p.name, args.regex)
        except Exception as e: print(f"[skip] {p.name}: {e}"); continue
        rec=per_file_deltaF(p, T, cstar, args.require_col)
        if rec is not None: recs.append(rec)

    if len(recs)<3: raise SystemExit("Too few valid records.")
    df=pd.DataFrame(recs)
    agg=aggregate_by_T(df)
    out_prefix=f"L{args.L}"
    agg.to_csv(data_dir/f"{out_prefix}_DeltaF_aggregated.csv", index=False)

    # 窓抽出＆零点
    T_lo,T_hi=min(args.twin),max(args.twin)
    win=agg[(agg["T"]>=T_lo)&(agg["T"]<=T_hi)].sort_values("T").copy()
    Ti=win["T"].to_numpy(); Fi=win["DeltaF"].to_numpy()
    z,Fi_fit,inc = (np.nan, np.array([]), True)
    method_note="isotonic(auto)"
    if len(Ti)>=2:
        # まずisotonicを実行（プロット用に常にフィット結果が必要なため）
        z_iso, Fi_fit, inc = isotonic_zero_auto(Ti, Fi)

        # 窓内に符号反転があるか確認
        has_root = (np.nanmin(Fi) < 0) and (np.nanmax(Fi) > 0)
        if has_root:
            z = z_iso
            method_note = f"isotonic(increasing={inc})"
            # フォールバック: isotonicがNaNを返した場合、隣接線形補間に切り替える
            if not np.isfinite(z):
                z = find_zero_linear(Ti, Fi)
                method_note = "bracket_linear"
        else:
            # 窓内に符号反転がなければ、NaN確定（外挿禁止）
            z = np.nan
            method_note = "no_root_in_window"

    # bootstrap（符号反転標本のみ）
    rng=np.random.RandomState(123); groups={T:g.index.to_numpy() for T,g in df.groupby("T")}
    T_sorted=np.array(sorted([t for t in groups.keys() if (t>=T_lo and t<=T_hi)]))
    boots=[]
    for b in range(args.n_boot):
        rows=[]
        for T in T_sorted:
            idx=groups[T]; take=rng.choice(idx, size=len(idx), replace=True)
            g=df.loc[take]; w=1.0/np.maximum(g["se"].to_numpy(),1e-12)**2
            mu=float(np.sum(w*g["DeltaF_signed"])/np.sum(w))
            rows.append((float(T),mu))
        rows.sort(key=lambda t:t[0]); Tb=np.array([t for t,_ in rows]); Fb=np.array([f for _,f in rows])
        if len(Tb)<2: continue
        if not (np.nanmin(Fb) < 0 < np.nanmax(Fb)): continue
        
        # bootstrapでもフォールバックを適用
        zb_iso,_,_ = isotonic_zero_auto(Tb, Fb)
        zb = zb_iso
        if not np.isfinite(zb):
            zb = find_zero_linear(Tb, Fb)

        if np.isfinite(zb): boots.append(zb)
    z_med=float(np.median(boots)) if boots else np.nan
    CI=(np.nan,np.nan)
    if len(boots)>=20:
        lo,hi=np.percentile(boots,[2.5,97.5]); CI=(float(lo),float(hi))

    # 保存＆図
    meta={"L":args.L,"method":f"bundles={args.bundles}, exclude={args.exclude_substr}, require_col={args.require_col}, {method_note}",
          "cstar":cstar,"T_window":[T_lo,T_hi],
          "T_sym_point": float(z) if np.isfinite(z) else None,
          "T_sym_bootstrap_median": float(z_med) if np.isfinite(z_med) else None,
          "CI_95":[float(CI[0]) if np.isfinite(CI[0]) else None, float(CI[1]) if np.isfinite(CI[1]) else None],
          "n_files_used": int(len(df)),"n_temps_used":int(len(win)),"n_boot":int(args.n_boot)}
    with open(data_dir/f"L{args.L}_Tsym_reconciled.json","w",encoding="utf-8") as f: json.dump(meta,f,ensure_ascii=False,indent=2)
    plot_monotone(args.L, agg["T"].to_numpy(), agg["DeltaF"].to_numpy(),
                  Ti, Fi_fit if len(Ti)>0 else np.array([]), z, data_dir/f"L{args.L}_DeltaF_monotone_fit.pdf", method_note)
    print(f"Saved: L{args.L}_Tsym_reconciled.json, _DeltaF_aggregated.csv, _DeltaF_monotone_fit.pdf")
    if np.isfinite(z): print(f"T_sym(point) = {z:.6f}")
    if np.isfinite(z_med): print(f"T_sym(bootstrap median) = {z_med:.6f}  95%CI=({CI[0]:.6f}, {CI[1]:.6f})")

if __name__=="__main__":
    os.environ.setdefault("OMP_NUM_THREADS","1"); os.environ.setdefault("MKL_NUM_THREADS","1")
    main()
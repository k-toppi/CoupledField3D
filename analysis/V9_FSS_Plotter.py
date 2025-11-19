import pandas as pd
import numpy as np
from scipy.stats import chi2

# --- 重要な修正：バックエンドの指定と、テキストのアウトライン化を強制的に無効化 ---
import matplotlib
matplotlib.use("pdf")  # バックエンドをPDFに強制指定
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['text.usetex'] = False      # TeX経由の描画を明示的に無効化
matplotlib.rcParams['svg.fonttype'] = 'none'    # SVGでのアウトライン化も抑制
import matplotlib.pyplot as plt
# ------------------------------------------------------------------------------------

def perform_fss_analysis(csv_path='T_sym_table.csv', nu=0.63):
    """
    T_sym_table.csvを読み込み、FSS解析を実行し、結果とグラフを生成する。
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"エラー: {csv_path} が見つかりません。")
        return

    # --- データ準備 ---
    df['inv_L_nu'] = df['L']**(-1/nu)
    df['sigma'] = (df['CI_high'] - df['CI_low']) / 3.92
    df['weight'] = 1 / df['sigma']**2

    x = df['inv_L_nu'].values
    y = df['T_sym'].values
    w = df['weight'].values
    sigma = df['sigma'].values

    # --- モデルA: 重み付き一次回帰 ---
    p_weighted, cov_weighted = np.polyfit(x, y, 1, w=w, cov=True)
    a_w, tc_w = p_weighted
    y_fit_w = a_w * x + tc_w
    residuals_w = y - y_fit_w
    chi2_w = np.sum(((residuals_w) / sigma)**2)
    ndf_w = len(x) - 2
    chi2_per_ndf_w = chi2_w / ndf_w

    # --- モデルB: 等重み一次回帰 ---
    p_unweighted = np.polyfit(x, y, 1)
    a_uw, tc_uw = p_unweighted

    # --- 最終Tcの決定 ---
    tc_final_center = (tc_w + tc_uw) / 2
    tc_final_error = abs(tc_w - tc_uw) / 2

    # --- 結果の表示 ---
    print("--- V9プロジェクト最終結論：FSS外挿解析結果 ---")
    print("\n[モデルA: 重み付き一次回帰 (主結果)]")
    print(f"  臨界温度 (Tc): {tc_w:.5f}")
    print(f"  傾き (a): {a_w:.2f}")
    print(f"  χ²/ndf: {chi2_per_ndf_w:.4f}")

    print("\n[モデルB: 等重み一次回帰 (補助結果)]")
    print(f"  臨界温度 (Tc): {tc_uw:.5f}")

    print("\n[最終結論]")
    print(f"  最終的な臨界温度 (Tc): {tc_final_center:.4f} ± {tc_final_error:.4f}")
    print("-" * 50)

    # --- グラフの生成 ---
    plt.style.use('default')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), dpi=150, sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    
    # 上段：FSSプロット
    ax1.errorbar(x, y, yerr=sigma, fmt='o', color='blue', capsize=5, label='T_sym(L) (1σ error)')
    x_fit = np.array([0, x.max()])
    y_fit_line = a_w * x_fit + tc_w
    ax1.plot(x_fit, y_fit_line, '--', color='red', label=f'Weighted Fit (Tc={tc_w:.5f})')
    ax1.plot(0, tc_w, '*', color='red', markersize=15, label=f'Extrapolated Tc')
    ax1.set_ylabel('T_sym(L)')
    ax1.set_title('Final FSS Plot (ν=0.63)')
    ax1.legend()
    ax1.grid(True)

    # 下段：残差プロット
    ax2.errorbar(x, residuals_w / sigma, yerr=1, fmt='o', color='green', capsize=5)
    ax2.axhline(0, color='black', linestyle='--', lw=1)
    ax2.set_xlabel('L^(-1/ν)')
    ax2.set_ylabel('Normalized Residuals\n(y - fit) / σ')
    ax2.set_ylim(-2.5, 2.5)
    ax2.grid(True)

    plt.tight_layout()
    fig.savefig("FSS_Final_Plot.pdf")
    plt.close(fig)
    print("\nグラフを 'FSS_Final_Plot.pdf' として保存しました。")

if __name__ == '__main__':
    perform_fss_analysis()
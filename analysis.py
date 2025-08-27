# =================================================================
# analysis.py (Publication Version)
#
# 目的:
#   simulation.pyによって生成されたCSVデータを読み込み、
#   論文のFig.1 (エネルギー保存)とFig.2 (有効質量の影響)を
#   PDFファイルとして生成する。
#
# 実行方法:
#   python analysis.py
#
# 依存ファイル:
#   - M50_data.csv (Fig.1 と Fig.2 の標準データ用)
#   - M25_data.csv (Fig.2 の比較データ用)
#   - M100_data.csv (Fig.2 の比較データ用)
# =================================================================

import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_fig1(data_path='M50_data.csv'):
    """Fig.1: エネルギーと粒子数の保存誤差をプロット"""
    print(f"--- Generating Fig.1 from {data_path} ---")
    if not os.path.exists(data_path):
        print(f"[Error] Data file not found: {data_path}. Please run simulation first.")
        return

    df = pd.read_csv(data_path)
    fig, ax1 = plt.subplots(figsize=(10, 6))
    initial_energy = df['E_total'].iloc[0]

    ax1.set_xlabel('Time t (dimensionless)')
    ax1.set_ylabel('Total Energy (dimensionless)', color='black')
    ax1.plot(df['time'], df['E_total'], color='black', label='Total Energy Drift')
    ax1.axhline(y=initial_energy, color='gray', linestyle='--', label=f'Initial Energy ({initial_energy:.3f})')
    ax1.tick_params(axis='y', labelcolor='black')

    ax2 = ax1.twinx()
    particle_deviation = df['norm'] - 1.0
    ax2.set_ylabel('Particle Number Deviation (N-1)', color='tab:blue')
    ax2.plot(df['time'], particle_deviation, color='tab:blue', linestyle='--')
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.yaxis.set_major_formatter(plt.FormatStrFormatter('%.1e'))

    fig.suptitle('Fig. S1: Analysis of Conservation Laws in Numerical Simulation')
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper right')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    plt.savefig("fig1.pdf")
    print("-> fig1.pdf saved successfully.")
    plt.close(fig)

def generate_fig2(paths={'M25':'M25_data.csv', 'M50':'M50_data.csv', 'M100':'M100_data.csv'}):
    """Fig.2: 有効質量Mの影響を比較プロット"""
    print("--- Generating Fig.2 from multiple data files ---")
    
    plot_info = {
        'M25': {'label': 'Barrier (M=25, Lighter & Unstable)', 'color': 'red', 'linestyle': ':'},
        'M50': {'label': 'Barrier (M=50, Standard & Stable)', 'color': 'black', 'linestyle': '-', 'linewidth': 2.0},
        'M100': {'label': 'Barrier (M=100, Heavier & Stable)', 'color': 'blue', 'linestyle': '--'}
    }
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    all_files_found = True
    for key, path in paths.items():
        if not os.path.exists(path):
            print(f"[Error] Data file not found: {path}. Please run all required simulations first.")
            all_files_found = False
    if not all_files_found: return

    for key, path in paths.items():
        df = pd.read_csv(path)
        info = plot_info[key]
        ax.plot(df['time'], df['z_barrier_pos'], **info)

    ax.set_title('Fig. S2: Effect of Effective Mass (M) on System Dynamics')
    ax.set_xlabel('Time t (dimensionless)')
    ax.set_ylabel('Position of Barrier (z)')
    ax.legend()
    ax.grid(True)
    ax.set_ylim(-35, 5)
    
    plt.savefig("fig2.pdf")
    print("-> fig2.pdf saved successfully.")
    plt.close(fig)

if __name__ == '__main__':
    print("========================================")
    print("   Publication Figure Generator   ")
    print("========================================")
    generate_fig1()
    generate_fig2()
    print("\nAll figures generated.")
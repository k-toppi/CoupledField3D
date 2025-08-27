# -*- coding: utf-8 -*-
# ===================================================================
# plot_all_figures.py
# Author: Toshiya Konno & Gemini
# Date: 2025-07-30
#
# Description:
# このスクリプトを実行するだけで. 論文に必要な全ての図が自動で再生成され.
# 対応するフォルダにPDFデータが保存されます. これにより. 誰でも我々の最終的な
# 視覚的成果を完全に再現できます.
#
# Usage:
# python plot_all_figures.py
# ===================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Global Plotting Settings ---
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['mathtext.fontset'] = 'cm'

# --- Define Input/Output Directories ---
# Assumes this script is in 'reproducibility_test'
BASE_PATH = "."
OUTPUT_DIR = os.path.join(BASE_PATH, "01_Figures_Reproduced") # Use a new folder to avoid overwriting originals

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# --- Figure 2: High-Significance Scan ---
def plot_figure2():
    print("Plotting Figure 2...")
    try:
        df = pd.read_csv(os.path.join(BASE_PATH, "04_Universality_Data", "SNR_vs_T_gamma_1.5.csv"))
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.errorbar(df['Temperature'], df['Mean_SNR'], yerr=df['SEM_SNR'], fmt='-o', capsize=5, label='γ = 1.5')
        ax.set_xlabel('Thermal Strength T ($k_B T$)')
        ax.set_ylabel('Signal-to-Noise Ratio (SNR) [dB]')
        ax.set_title('Stochastic Resonance: High-Significance Scan (γ = 1.5, N=100)')
        ax.grid(True, linestyle='--', linewidth=0.5)
        plt.savefig(os.path.join(OUTPUT_DIR, "fig2_snr_high_stats.pdf"), bbox_inches='tight')
        plt.close()
        print("... Figure 2 saved successfully.")
    except FileNotFoundError:
        print("... ERROR: CSV file for Figure 2 not found. Please run simulations first.")

# --- Figure 3: Universality of SR ---
def plot_figure3():
    print("Plotting Figure 3...")
    try:
        df10 = pd.read_csv(os.path.join(BASE_PATH, "04_Universality_Data", "SNR_vs_T_gamma_1.0.csv"))
        df15 = pd.read_csv(os.path.join(BASE_PATH, "04_Universality_Data", "SNR_vs_T_gamma_1.5.csv"))
        df20 = pd.read_csv(os.path.join(BASE_PATH, "04_Universality_Data", "SNR_vs_T_gamma_2.0.csv"))
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.errorbar(df10['Temperature'], df10['Mean_SNR'], yerr=df10['SEM_SNR'], fmt='-o', capsize=3, label='γ = 1.0')
        ax.errorbar(df15['Temperature'], df15['Mean_SNR'], yerr=df15['SEM_SNR'], fmt='-o', capsize=3, label='γ = 1.5')
        ax.errorbar(df20['Temperature'], df20['Mean_SNR'], yerr=df20['SEM_SNR'], fmt='-o', capsize=3, label='γ = 2.0')
        ax.set_xlabel('Thermal Strength T ($k_B T$)')
        ax.set_ylabel('Signal-to-Noise Ratio (SNR) [dB]')
        ax.set_title('Universality of Stochastic Resonance: SNR vs. T for different γ')
        ax.legend(title="Dissipation Strength")
        ax.grid(True, linestyle='--', linewidth=0.5)
        plt.savefig(os.path.join(OUTPUT_DIR, "fig3_snr_gamma_sweep.pdf"), bbox_inches='tight')
        plt.close()
        print("... Figure 3 saved successfully.")
    except FileNotFoundError:
        print("... ERROR: CSV files for Figure 3 not found. Please run simulations first.")

# --- Figure 4: Control Experiment ---
def plot_figure4():
    print("Plotting Figure 4...")
    try:
        df = pd.read_csv(os.path.join(BASE_PATH, "05_Control_Experiment", "Control_Experiment_SNR_vs_T_ClassicalOnly.csv"))
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.errorbar(df['Temperature'], df['Mean_SNR'], yerr=df['SEM_SNR'], fmt='-o', capsize=5, color='red', label='Classical Only (No Feedback)')
        ax.axhline(0, ls='--', color='gray', lw=1, label='Reference (0 dB)')
        ax.set_xlabel('Thermal Strength T ($k_B T$)')
        ax.set_ylabel('Signal-to-Noise Ratio (SNR) [dB]')
        ax.set_title('Control Experiment: SNR in a Purely Classical System')
        ax.legend()
        ax.grid(True, linestyle='--', linewidth=0.5)
        plt.savefig(os.path.join(OUTPUT_DIR, "fig4_control_experiment.pdf"), bbox_inches='tight')
        plt.close()
        print("... Figure 4 saved successfully.")
    except FileNotFoundError:
        print("... ERROR: CSV file for Figure 4 not found. Please run simulations first.")

# --- Figure A1 (now 5): Strong Damping ---
def plot_figureA1():
    print("Plotting Figure A1 (Strong Damping)...")
    try:
        df = pd.read_csv(os.path.join(BASE_PATH, "06_Supplementary_StrongDamping", "SNR_vs_T_gamma_2.5.csv"))
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.errorbar(df['Temperature'], df['Mean_SNR'], yerr=df['SEM_SNR'], fmt='-o', capsize=5, color='purple', label='γ = 2.5 (Strong Damping)')
        ax.set_xlabel('Thermal Strength T ($k_B T$)')
        ax.set_ylabel('Signal-to-Noise Ratio (SNR) [dB]')
        ax.set_title('SNR in Strongly Damped Regime')
        ax.legend()
        ax.grid(True, linestyle='--', linewidth=0.5)
        ax.axhline(0, ls='--', color='gray', lw=1)
        plt.savefig(os.path.join(OUTPUT_DIR, "figA1_strong_damping.pdf"), bbox_inches='tight')
        plt.close()
        print("... Figure A1 saved successfully.")
    except FileNotFoundError:
        print("... ERROR: CSV file for Figure A1 not found. Please run simulations first.")

# --- Figure A2 (now 6): Effective Potential ---
def plot_figureA2():
    print("Plotting Figure A2 (Effective Potential)...")
    # This figure does not depend on simulation data, but on parameters.
    A = 0.1
    g = -15.0
    sigma = 4.0
    sigma_soliton = 1.0
    norm_factor = 1 / (sigma_soliton * np.sqrt(2 * np.pi))
    z = np.linspace(-10, 10, 1000)
    V_barrier = A * np.exp(-z**2 / (2 * sigma**2))
    psi_squared = norm_factor * np.exp(-z**2 / (2 * sigma_soliton**2))
    V_self = g * psi_squared
    V_eff = V_barrier + V_self
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(z, V_barrier, 'r--', label='Barrier Potential ($V_{barrier}$)')
    ax.plot(z, V_self, 'b--', label='Self-Trapping Potential ($g|\\psi|^2$)')
    ax.plot(z, V_eff, 'k-', linewidth=2, label='Effective Potential ($V_{eff}$)')
    ax.set_xlabel('Position z (dimensionless)')
    ax.set_ylabel('Potential Energy (dimensionless)')
    ax.set_title('Effective Potential Landscape for the Soliton')
    ax.legend()
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.set_ylim(V_self.min() - 1, V_barrier.max() + 1)
    ax.set_xlim(-10, 10)
    plt.savefig(os.path.join(OUTPUT_DIR, "figA2_effective_potential.pdf"), bbox_inches='tight')
    plt.close()
    print("... Figure A2 saved successfully.")

# --- Main Execution ---
if __name__ == "__main__":
    print("Plotting all figures for the paper...")
    # Note: Figure 1 (Phase Diagram) is assumed to be pre-generated and is not reproduced here.
    plot_figure2()
    plot_figure3()
    plot_figure4()
    plot_figureA1()
    plot_figureA2()
    print(f"\nAll figures plotted successfully and saved in '{OUTPUT_DIR}' directory.")
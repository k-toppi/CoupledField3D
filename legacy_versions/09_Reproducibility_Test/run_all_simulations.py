# -*- coding: utf-8 -*-
# ===================================================================
# run_all_simulations.py
# Author: Toshiya Konno & Gemini
# Date: 2025-07-30
#
# Description:
# このスクリプト一つを実行するだけで. 論文に必要な全てのシミュレーションが自動で実行され.
# 対応するフォルダにCSVデータが保存されます. これにより. 誰でも我々の生データを完全に再現できます.
#
# Usage:
# python run_all_simulations.py
# ===================================================================

import numpy as np
import pandas as pd
from scipy.signal import welch
from tqdm import tqdm
import os

# --- Global Simulation Parameters ---
M = 50.0
k_mech = 10.0
k_B = 1.0
dt = 0.005
T_total = 200.0
N_steps = int(T_total / dt)
t_coords = np.linspace(0, T_total, N_steps)
N_runs = 100
T_values = np.linspace(0.0, 0.5, 26)
A_signal = 0.01
f_signal = np.sqrt(k_mech / M) / (2 * np.pi)

# --- Helper Functions ---
def get_forces(z, v, t_val, T, gamma, feedback_on=True):
    """Calculates the total force on the barrier."""
    F_restoring = -k_mech * z
    F_dissipation = -gamma * v
    F_thermal = np.sqrt(2 * gamma * k_B * T / dt) * np.random.normal(0, 1)
    
    F_signal_term = 0.0
    if feedback_on:
        # This term simulates the quantum feedback as a weak periodic signal
        F_signal_term = A_signal * np.cos(2 * np.pi * f_signal * t_val)
        
    return F_restoring + F_dissipation + F_thermal + F_signal_term

def calculate_snr_welch(trajectory, dt, f_signal):
    """Calculates SNR using Welch's method for stability."""
    fs = 1.0 / dt
    nperseg = len(trajectory) // 8
    f, Pxx = welch(trajectory, fs, nperseg=nperseg)
    
    signal_idx = np.argmin(np.abs(f - f_signal))
    signal_power = Pxx[signal_idx]
    
    noise_indices = (np.abs(f - f_signal) > 2 * (f[1]-f[0])) & (f > 0)
    noise_power = np.mean(Pxx[noise_indices])
    
    return 10 * np.log10(signal_power / noise_power) if noise_power > 0 else -np.inf

def run_simulation_set(gamma, feedback_on, output_dir, filename):
    """Runs a full set of simulations for a given gamma and feedback state."""
    # Using English for console output to avoid any potential encoding issues.
    print(f"\nRunning simulation set for gamma={gamma} (Feedback: {feedback_on})...")
    results = []
    for T in tqdm(T_values, desc=f"gamma={gamma}"):
        snr_runs = []
        for _ in range(N_runs):
            z, v = 0.0, 0.0
            z_trajectory = np.zeros(N_steps)
            for i in range(N_steps):
                F = get_forces(z, v, t_coords[i], T, gamma, feedback_on)
                a = F / M
                v += a * dt
                z += v * dt
                z_trajectory[i] = z
            
            transient_steps = N_steps // 2
            snr = calculate_snr_welch(z_trajectory[transient_steps:], dt, f_signal)
            snr_runs.append(snr)
            
        mean_snr = np.mean(snr_runs)
        sem_snr = np.std(snr_runs) / np.sqrt(N_runs)
        results.append({'Temperature': T, 'Mean_SNR': mean_snr, 'SEM_SNR': sem_snr})
        
    df = pd.DataFrame(results)
    
    # Create directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    full_path = os.path.join(output_dir, filename)
    df.to_csv(full_path, index=False)
    print(f"Data saved to {full_path}")

# --- Main Execution ---
if __name__ == "__main__":
    print("Starting all simulations for the paper...")
    
    # Define relative paths for output directories
    # This assumes the script is run from a directory like 'reproducibility_test'
    # and the data folders are at the same level.
    base_path = "." 
    
    # Data for Figure 3 (Universality)
    dir_fig3 = os.path.join(base_path, "04_Universality_Data")
    run_simulation_set(gamma=1.0, feedback_on=True, output_dir=dir_fig3, filename="SNR_vs_T_gamma_1.0.csv")
    run_simulation_set(gamma=1.5, feedback_on=True, output_dir=dir_fig3, filename="SNR_vs_T_gamma_1.5.csv")
    run_simulation_set(gamma=2.0, feedback_on=True, output_dir=dir_fig3, filename="SNR_vs_T_gamma_2.0.csv")

    # Data for Figure 4 (Control Experiment)
    dir_fig4 = os.path.join(base_path, "05_Control_Experiment")
    run_simulation_set(gamma=1.5, feedback_on=False, output_dir=dir_fig4, filename="Control_Experiment_SNR_vs_T_ClassicalOnly.csv")

    # Data for Figure A1 (Strong Damping)
    dir_figA1 = os.path.join(base_path, "06_Supplementary_StrongDamping")
    run_simulation_set(gamma=2.5, feedback_on=True, output_dir=dir_figA1, filename="SNR_vs_T_gamma_2.5.csv")
    
    print("\nAll simulations completed successfully.")
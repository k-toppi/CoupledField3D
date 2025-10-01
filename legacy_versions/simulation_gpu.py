# =================================================================
# simulation_gpu.py (GPU Version for Publication)
#
# 目的:
#   CUDA対応GPUを持つ環境で高速に実行するためのバージョン。
#   論文で定義された3D結合場のシミュレーションを実行し、
#   解析用の時系列データをCSVファイルとして保存する。
#   このコードが高解像度の論文掲載図を生成します。
# =================================================================

import numpy as np
import cupy as cp # NumPyではなくCuPyを使用
import time
import os
import csv
import argparse

def run_simulation(kz_kick, mass_barrier, k_spring, total_time, output_filename):
    """論文の物理モデルに基づいたシミュレーションを実行する (GPU版)"""
    print(f"--- GPU Simulation Start: M={mass_barrier}, k={k_spring}, T={total_time} ---")
    print(f"Output will be saved to: {output_filename}")

    # --- 1. グリッドと物理パラメータ (高解像度) ---
    Nx, Ny, Nz = 64, 64, 256
    Lx, Ly, Lz = 12.0, 12.0, 48.0
    dt, Nt = 5e-6, int(total_time / 5e-6) # GPUなので高精度な時間ステップ

    g_nonlinear = -15.0
    barrier_A = 0.1
    barrier_sigma = 4.0
    z0_barrier_initial = -10.0
    m_particle = 1.0

    # --- 2. 波数空間 ---
    x = cp.linspace(-Lx/2, Lx/2, Nx); y = cp.linspace(-Ly/2, Ly/2, Ny); z = cp.linspace(-Lz/2, Lz/2, Nz)
    dx, dy, dz = float(x[1]-x[0]), float(y[1]-y[0]), float(z[1]-z[0])
    X, Y, Z = cp.meshgrid(x, y, z, indexing='ij')
    kx = 2*cp.pi*cp.fft.fftfreq(Nx,d=dx); ky = 2*cp.pi*cp.fft.fftfreq(Ny,d=dy); kz = 2*cp.pi*cp.fft.fftfreq(Nz,d=dz)
    Kx, Ky, Kz = cp.meshgrid(kx, ky, kz, indexing='ij')
    K2 = Kx**2 + Ky**2 + Kz**2
    exp_K = cp.exp(-0.5j * (K2 / (2 * m_particle)) * dt)

    # --- 3. ポテンシャルと力の定義 ---
    V_trap = 0.5 * 1.0 * (X**2 + Y**2)

    def get_V_barrier(z_pos):
        return barrier_A * cp.exp(-((Z - z_pos)**2) / (2 * barrier_sigma**2))

    def get_force_HF(psi, z_pos):
        V_b = get_V_barrier(z_pos)
        dV_dzb = V_b * (Z - z_pos) / barrier_sigma**2
        force = -cp.sum(cp.conj(psi) * dV_dzb * psi).real * dx * dy * dz
        return force

    def get_force_restoring(z_pos):
        return -k_spring * (z_pos - z0_barrier_initial)

    # --- 4. エネルギー計算の定義 ---
    def get_energy(psi, V_total, z_pos, v_barrier):
        psi_k = cp.fft.fftn(psi)
        E_kin_q = cp.sum(cp.conj(psi_k) * (K2 / (2 * m_particle)) * psi_k).real / (Nx*Ny*Nz) * dx*dy*dz
        E_pot_q = cp.sum(cp.conj(psi) * V_total * psi).real * dx*dy*dz
        E_kin_c = 0.5 * mass_barrier * v_barrier**2
        return E_kin_q + E_pot_q + E_kin_c

    # --- 5. 初期状態 ---
    psi = cp.exp(-((X**2 + Y**2)/(2*1.0**2) + (Z - (-20.0))**2 / (2*2.0**2)), dtype=cp.complex128)
    psi *= cp.exp(1j * kz_kick * Z)
    norm = cp.sqrt(cp.sum(cp.abs(psi)**2) * dx * dy * dz)
    psi /= norm

    z_b = cp.array(z0_barrier_initial, dtype=cp.float64)
    v_b = cp.array(0.0, dtype=cp.float64)

    # --- 6. シミュレーションループ ---
    print("Main loop starting...")
    start_time = time.time()
    with open(output_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'z_barrier_pos', 'E_total', 'norm'])

        for n in range(Nt + 1):
            if n % 2000 == 0:
                V_b = get_V_barrier(z_b)
                V_nl = g_nonlinear * cp.abs(psi)**2
                V_total = V_trap + V_b + V_nl
                current_energy = get_energy(psi, V_total, z_b, v_b)
                current_norm = cp.sum(cp.abs(psi)**2) * dx * dy * dz
                writer.writerow([n * dt, float(z_b.get()), float(current_energy.get()), float(current_norm.get())])
                if n % 20000 == 0:
                    print(f"Step {n}/{Nt}, Time: {n*dt:.2f}, Barrier Z: {float(z_b.get()):.3f}")

            V_b = get_V_barrier(z_b)
            V_nl = g_nonlinear * cp.abs(psi)**2
            V_total = V_trap + V_b + V_nl
            psi *= cp.exp(-0.5j * V_total * dt)
            psi_k = cp.fft.fftn(psi)
            psi_k *= exp_K
            psi = cp.fft.ifftn(psi_k)
            force_hf = get_force_HF(psi, z_b)
            force_res = get_force_restoring(z_b)
            v_b += ((force_hf + force_res) / mass_barrier) * dt
            z_b += v_b * dt
            V_b = get_V_barrier(z_b)
            V_nl = g_nonlinear * cp.abs(psi)**2
            V_total = V_trap + V_b + V_nl
            psi *= cp.exp(-0.5j * V_total * dt)

    print(f"--- Simulation Finished. Total time: {time.time() - start_time:.2f} sec ---")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="3D Coupled Field Simulation (GPU Version)")
    parser.add_argument('--kz', type=float, default=0.15, help='Initial momentum kick')
    parser.add_argument('--mass', type=float, default=50.0, help='Effective mass of the barrier')
    parser.add_argument('--k', type=float, default=10.0, help='Spring constant')
    parser.add_argument('--time', type=float, default=40.0, help='Total simulation time')
    parser.add_argument('--output', type=str, required=True, help='Output CSV filename (e.g., M50_data.csv)')
    args = parser.parse_args()
    run_simulation(args.kz, args.mass, args.k, args.time, args.output)# =================================================================
# simulation_gpu.py (GPU Version for Publication)
#
# 目的:
#   CUDA対応GPUを持つ環境で高速に実行するためのバージョン。
#   論文で定義された3D結合場のシミュレーションを実行し、
#   解析用の時系列データをCSVファイルとして保存する。
#   このコードが高解像度の論文掲載図を生成します。
# =================================================================

import numpy as np
import cupy as cp # NumPyではなくCuPyを使用
import time
import os
import csv
import argparse

def run_simulation(kz_kick, mass_barrier, k_spring, total_time, output_filename):
    """論文の物理モデルに基づいたシミュレーションを実行する (GPU版)"""
    print(f"--- GPU Simulation Start: M={mass_barrier}, k={k_spring}, T={total_time} ---")
    print(f"Output will be saved to: {output_filename}")

    # --- 1. グリッドと物理パラメータ (高解像度) ---
    Nx, Ny, Nz = 64, 64, 256
    Lx, Ly, Lz = 12.0, 12.0, 48.0
    dt, Nt = 5e-6, int(total_time / 5e-6) # GPUなので高精度な時間ステップ

    g_nonlinear = -15.0
    barrier_A = 0.1
    barrier_sigma = 4.0
    z0_barrier_initial = -10.0
    m_particle = 1.0

    # --- 2. 波数空間 ---
    x = cp.linspace(-Lx/2, Lx/2, Nx); y = cp.linspace(-Ly/2, Ly/2, Ny); z = cp.linspace(-Lz/2, Lz/2, Nz)
    dx, dy, dz = float(x[1]-x[0]), float(y[1]-y[0]), float(z[1]-z[0])
    X, Y, Z = cp.meshgrid(x, y, z, indexing='ij')
    kx = 2*cp.pi*cp.fft.fftfreq(Nx,d=dx); ky = 2*cp.pi*cp.fft.fftfreq(Ny,d=dy); kz = 2*cp.pi*cp.fft.fftfreq(Nz,d=dz)
    Kx, Ky, Kz = cp.meshgrid(kx, ky, kz, indexing='ij')
    K2 = Kx**2 + Ky**2 + Kz**2
    exp_K = cp.exp(-0.5j * (K2 / (2 * m_particle)) * dt)

    # --- 3. ポテンシャルと力の定義 ---
    V_trap = 0.5 * 1.0 * (X**2 + Y**2)

    def get_V_barrier(z_pos):
        return barrier_A * cp.exp(-((Z - z_pos)**2) / (2 * barrier_sigma**2))

    def get_force_HF(psi, z_pos):
        V_b = get_V_barrier(z_pos)
        dV_dzb = V_b * (Z - z_pos) / barrier_sigma**2
        force = -cp.sum(cp.conj(psi) * dV_dzb * psi).real * dx * dy * dz
        return force

    def get_force_restoring(z_pos):
        return -k_spring * (z_pos - z0_barrier_initial)

    # --- 4. エネルギー計算の定義 ---
    def get_energy(psi, V_total, z_pos, v_barrier):
        psi_k = cp.fft.fftn(psi)
        E_kin_q = cp.sum(cp.conj(psi_k) * (K2 / (2 * m_particle)) * psi_k).real / (Nx*Ny*Nz) * dx*dy*dz
        E_pot_q = cp.sum(cp.conj(psi) * V_total * psi).real * dx*dy*dz
        E_kin_c = 0.5 * mass_barrier * v_barrier**2
        return E_kin_q + E_pot_q + E_kin_c

    # --- 5. 初期状態 ---
    psi = cp.exp(-((X**2 + Y**2)/(2*1.0**2) + (Z - (-20.0))**2 / (2*2.0**2)), dtype=cp.complex128)
    psi *= cp.exp(1j * kz_kick * Z)
    norm = cp.sqrt(cp.sum(cp.abs(psi)**2) * dx * dy * dz)
    psi /= norm

    z_b = cp.array(z0_barrier_initial, dtype=cp.float64)
    v_b = cp.array(0.0, dtype=cp.float64)

    # --- 6. シミュレーションループ ---
    print("Main loop starting...")
    start_time = time.time()
    with open(output_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'z_barrier_pos', 'E_total', 'norm'])

        for n in range(Nt + 1):
            if n % 2000 == 0:
                V_b = get_V_barrier(z_b)
                V_nl = g_nonlinear * cp.abs(psi)**2
                V_total = V_trap + V_b + V_nl
                current_energy = get_energy(psi, V_total, z_b, v_b)
                current_norm = cp.sum(cp.abs(psi)**2) * dx * dy * dz
                writer.writerow([n * dt, float(z_b.get()), float(current_energy.get()), float(current_norm.get())])
                if n % 20000 == 0:
                    print(f"Step {n}/{Nt}, Time: {n*dt:.2f}, Barrier Z: {float(z_b.get()):.3f}")

            V_b = get_V_barrier(z_b)
            V_nl = g_nonlinear * cp.abs(psi)**2
            V_total = V_trap + V_b + V_nl
            psi *= cp.exp(-0.5j * V_total * dt)
            psi_k = cp.fft.fftn(psi)
            psi_k *= exp_K
            psi = cp.fft.ifftn(psi_k)
            force_hf = get_force_HF(psi, z_b)
            force_res = get_force_restoring(z_b)
            v_b += ((force_hf + force_res) / mass_barrier) * dt
            z_b += v_b * dt
            V_b = get_V_barrier(z_b)
            V_nl = g_nonlinear * cp.abs(psi)**2
            V_total = V_trap + V_b + V_nl
            psi *= cp.exp(-0.5j * V_total * dt)

    print(f"--- Simulation Finished. Total time: {time.time() - start_time:.2f} sec ---")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="3D Coupled Field Simulation (GPU Version)")
    parser.add_argument('--kz', type=float, default=0.15, help='Initial momentum kick')
    parser.add_argument('--mass', type=float, default=50.0, help='Effective mass of the barrier')
    parser.add_argument('--k', type=float, default=10.0, help='Spring constant')
    parser.add_argument('--time', type=float, default=40.0, help='Total simulation time')
    parser.add_argument('--output', type=str, required=True, help='Output CSV filename (e.g., M50_data.csv)')
    args = parser.parse_args()
    run_simulation(args.kz, args.mass, args.k, args.time, args.output)
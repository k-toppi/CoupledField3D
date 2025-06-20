# =================================================================
# simulation.py
#
# 3D Coupled Field Simulation Code
# This script simulates the dynamics of a quantum soliton coupled with a
# classical, movable barrier, as described in the preprint:
# "A 3D Mathematical Model of a Dynamically Coupled Field..."
#
# Author: [先生の氏名]
# Version: 1.0 (for publication)
# License: MIT
# =================================================================

import numpy as np
import cupy as cp
import time
import os
import shutil
import csv
import argparse # For command-line arguments

def run_simulation(kz_kick, mass_barrier, k_spring, total_time):
    """
    Main function to run the simulation with given parameters.
    """
    print("===================================================")
    print(f"Starting simulation with: kz_kick={kz_kick}, M={mass_barrier}, k={k_spring}, T={total_time}")
    print("===================================================")

    # --- 1. Simulation Parameters ---
    # Grid settings
    Nx, Ny, Nz = 64, 64, 256
    Lx, Ly, Lz = 12.0, 12.0, 48.0

    # Time settings
    dt = 0.001  # Using a coarse dt for fast reconnaissance mode
    Nt = int(total_time / dt)

    # Physical parameters
    g_nonlinear_3D = -15.0
    barrier_height = 0.1
    barrier_smoothness = 4.0
    z0_barrier_initial = -10.0

    # I/O settings
    exp_name = f'sim_results_kz{kz_kick}_M{mass_barrier}_k{k_spring}'
    if os.path.exists(exp_name):
        shutil.rmtree(exp_name)
    os.makedirs(exp_name)
    csv_file_path = os.path.join(exp_name, 'trajectory_data.csv')
    print(f"Results will be saved in: ./{exp_name}/")

    # --- 2. Setup (GPU, Grids) ---
    try:
        cp.cuda.runtime.getDeviceCount()
        print("GPU successfully recognized.")
    except cp.cuda.runtime.CUDARuntimeError as e:
        print("GPU not found. This code requires a CUDA-enabled GPU and CuPy."); raise e

    x = cp.linspace(-Lx/2, Lx/2, Nx); y = cp.linspace(-Ly/2, Ly/2, Ny); z = cp.linspace(-Lz/2, Lz/2, Nz)
    X, Y, Z = cp.meshgrid(x, y, z, indexing='ij')
    dx, dy, dz = float(x[1]-x[0]), float(y[1]-y[0]), float(z[1]-z[0])
    kx = 2*cp.pi*cp.fft.fftfreq(Nx,d=dx); ky = 2*cp.pi*cp.fft.fftfreq(Ny,d=dy); kz = 2*cp.pi*cp.fft.fftfreq(Nz,d=dz)
    Kx, Ky, Kz = cp.meshgrid(kx, ky, kz, indexing='ij')
    K2 = Kx**2 + Ky**2 + Kz**2
    exp_K = cp.exp(-0.5j * K2 * dt)

    # --- 3. Helper Functions ---
    def update_potential(z_pos):
        return barrier_height * cp.exp(-((Z - z_pos)**2) / (2 * barrier_smoothness**2))

    def calculate_force(psi, z_pos):
        prob_density = cp.abs(psi)**2
        z_prob_density = cp.sum(prob_density, axis=(0, 1))
        peak_idx = cp.argmax(z_prob_density)
        z_peak = z[peak_idx]
        force = k_spring * (z_peak - z_pos)
        return force, z_peak

    # --- 4. Initial State ---
    print("Initializing wave function...")
    V_trap = 0.5 * 0.01 * (X**2 + Y**2)
    psi = cp.exp(-((X**2)/(2*1.0**2) + (Y**2)/(2*1.0**2) + (Z - (-20.0))**2 / (2*2.0**2)), dtype=cp.complex128)
    psi *= cp.exp(1j * kz_kick * Z)
    psi /= cp.sqrt(cp.sum(cp.abs(psi)**2) * dx * dy * dz)
    
    z_barrier_pos = cp.array(z0_barrier_initial, dtype=cp.float64)
    v_barrier = cp.array(0.0, dtype=cp.float64)
    print("Initialization complete.")

    # --- 5. Main Simulation Loop ---
    print(f"Starting main loop for {Nt} steps...")
    start_time = time.time()

    with open(csv_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'z_soliton_peak', 'z_barrier_pos'])

        for n in range(Nt + 1):
            # Split-step Fourier method
            V_barrier = update_potential(z_barrier_pos)
            V_nonlinear = g_nonlinear_3D * cp.abs(psi)**2
            V_total = V_trap + V_barrier + V_nonlinear
            
            psi *= cp.exp(-0.5j * V_total * dt)
            psi_k = cp.fft.fftn(psi)
            psi_k *= exp_K
            psi = cp.fft.ifftn(psi_k)
            
            force, z_soliton_peak = calculate_force(psi, z_barrier_pos)
            
            v_barrier += (force / mass_barrier) * dt
            z_barrier_pos += v_barrier * dt
            
            V_barrier = update_potential(z_barrier_pos)
            V_nonlinear = g_nonlinear_3D * cp.abs(psi)**2
            V_total = V_trap + V_barrier + V_nonlinear
            
            psi *= cp.exp(-0.5j * V_total * dt)

            # Record data
            if n % 100 == 0: # Record every 100 steps
                writer.writerow([n * dt, float(z_soliton_peak.get()), float(z_barrier_pos.get())])
                if n % 2000 == 0:
                    print(f"Step {n}/{Nt}, Time: {n*dt:.2f}, Barrier Z: {float(z_barrier_pos.get()):.3f}")

    end_time = time.time()
    print("\nSimulation finished.")
    print(f"Total computation time: {(end_time - start_time):.2f} seconds.")
    print(f"Data saved to: {csv_file_path}")

if __name__ == '__main__':
    # --- Argument Parser ---
    # This allows running the script from the command line with different parameters.
    # Example: python simulation.py --kz 0.15 --mass 50
    parser = argparse.ArgumentParser(description="3D Coupled Field Simulation")
    parser.add_argument('--kz', type=float, default=0.15, help='Initial momentum kick (kz_kick)')
    parser.add_argument('--mass', type=float, default=50.0, help='Effective mass of the barrier')
    parser.add_argument('--k', type=float, default=10.0, help='Spring constant for the restoring force')
    parser.add_argument('--time', type=float, default=40.0, help='Total simulation time')
    
    args = parser.parse_args()
    
    run_simulation(
        kz_kick=args.kz,
        mass_barrier=args.mass,
        k_spring=args.k,
        total_time=args.time
    )
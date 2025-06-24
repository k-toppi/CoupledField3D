# A 3D Mathematical Model of a Dynamically Coupled Field

This repository contains the simulation and analysis code for the paper:

**Title:** A 3D Mathematical Model of a Dynamically Coupled Field Inspired by Operator Algebras: Theoretical Foundation and Numerical Verification of Stable Coupled Motion  
**Author:** Toshiya Konno

The final version of the preprint is available on Zenodo:  
**DOI:** \[10.5281/zenodo.15718574](https://doi.org/10.5281/zenodo.15718574)

---

## Abstract

We propose a three-dimensional mathematical model that dynamically couples a quantum field and a single-degree-of-freedom classical barrier, inspired by operator-algebraic ideas. The quantum part is governed by a non-linear Gross–Pitaevskii equation, whereas the barrier follows Newtonian dynamics with a Hellmann–Feynman feedback force and a tensegrity-like restoring force. Extensive split-step Fourier simulations show that, for an attractive interaction g\<0 and an initial momentum within 0.1 \< k\_{z,kick} \<= 0.15, a self-trapped quantum soliton travels together with the barrier in a stable coupled motion. The state is robust against parameter fluctuations and external noise, suggesting a loss-less information-transport mechanism that could be relevant to intracellular processes. We detail the theoretical framework, numerical verification, limitations, and future extensions.

---

## Reproducibility

### Important Note on Reproducibility

The simulation data (`.csv` files) included in this repository were generated using the **CPU version** (`simulation.py`). This mode is designed to run on standard computers in a reasonable amount of time, allowing anyone to verify the code's functionality.

However, due to the reduced grid resolution for faster computation, the dynamics captured in this mode (especially the barrier's motion in Fig. 2\) are significantly less pronounced than those presented in the official publication.

**To reproduce the high-resolution figures published in the paper, it is necessary to run the `simulation_gpu.py` script on a CUDA-enabled GPU.** This process is computationally intensive and may take a considerable amount of time. The resulting data will fully match the beautiful dynamics shown in the preprint.

### How to Reproduce

#### 1\. Set up the Environment

It is highly recommended to use a virtual environment. The required packages are listed in `requirements.txt`.

\# Clone the repository

git clone https://github.com/k-toppi/CoupledField3D.git

cd CoupledField3D

\# Create and activate a virtual environment

python \-m venv venv

source venv/bin/activate  \# On macOS/Linux

\# venv\\Scripts\\activate    \# On Windows

\# Install the required packages

pip install \-r requirements.txt

#### 2\. Run the Simulation

This repository provides two versions of the simulation script:

- **For standard PCs (CPU only):** Use `simulation.py`. This will be slower but will work on any machine.  
    
  python simulation.py \--mass 50 \--output "M50\_data.csv"  
    
  python simulation.py \--mass 25 \--output "M25\_data.csv"  
    
  python simulation.py \--mass 100 \--output "M100\_data.csv"  
    
- **For PCs with an NVIDIA GPU:** Use `simulation_gpu.py` for much faster, high-resolution results. You will need to install `cupy` first: `pip install cupy-cudaXXX` (where `XXX` is your CUDA version).  
    
  python simulation\_gpu.py \--mass 50 \--output "M50\_data\_gpu.csv"  
    
  \# (and so on for other masses)

#### 3\. Generate the Figures

After generating the three data files (`.csv`) using either method, run the analysis script to create the figures.

python analysis.py

This will generate `fig1.pdf` and `fig2.pdf` in the current directory.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

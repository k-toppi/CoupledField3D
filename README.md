# A 3D Mathematical Model of a Dynamically Coupled Field

This repository contains the simulation and analysis code for the paper:

**Title:** A 3D Mathematical Model of a Dynamically Coupled Field Inspired by Operator Algebras: Theoretical Foundation and Numerical Verification of Stable Coupled Motion  
**Author:** Toshiya Konno

The final version of the preprint is available on Zenodo:  
**DOI:** [Link to Zenodo DOI will be added here upon publication]

---

## Abstract

We propose a three-dimensional mathematical model that dynamically couples a quantum field and a single-degree-of-freedom classical barrier, inspired by operator-algebraic ideas. The quantum part is governed by a non-linear Gross–Pitaevskii equation, whereas the barrier follows Newtonian dynamics with a Hellmann–Feynman feedback force and a tensegrity-like restoring force. Extensive split-step Fourier simulations show that, for an attractive interaction g<0 and an initial momentum within 0.1 < k_{z,kick} <= 0.15, a self-trapped quantum soliton travels together with the barrier in a stable coupled motion. The state is robust against parameter fluctuations and external noise, suggesting a loss-less information-transport mechanism that could be relevant to intracellular processes. We detail the theoretical framework, numerical verification, limitations, and future extensions.

---

## Reproducibility

### Computational Environment

The simulations and analyses were performed on Google Colaboratory. To ensure reproducibility, the specific environment used to generate the figures in the paper is detailed below.

- **Platform:** Google Colaboratory
- **Python Version:** 3.11.13
- **Key Libraries:**
  - `numpy==2.0.2`
  - `matplotlib==3.10.0`
  - `pandas==2.2.2` (Note: Pandas was part of the standard environment but not actively used in the core simulation scripts.)

A complete list of packages is available in the `requirements.txt` file.

### How to Reproduce

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/k-toppi/CoupledField3D.git
    cd CoupledField3D
    ```

2.  **Set up the Python environment:**
    It is highly recommended to use a virtual environment to avoid conflicts with other projects.
    ```bash
    # Create a virtual environment
    python3 -m venv venv
    
    # Activate it
    source venv/bin/activate  # On macOS/Linux
    # venv\Scripts\activate    # On Windows
    
    # Install the required packages
    pip install -r requirements.txt
    ```

3.  **Run the scripts:**
    - To reproduce the core simulation data: `python simulation.py`
    - To generate the figures (Fig.1, Fig.2) from the paper: `python analysis.py`

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

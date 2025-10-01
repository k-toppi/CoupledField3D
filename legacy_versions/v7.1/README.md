# A 3D Mathematical Model of a Dynamically Coupled Field Inspired by Operator Algebras: VII. Thermodynamically Consistent 3D Hybrid Model and Its Emergent Properties

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17083406.svg)](https://doi.org/10.5281/zenodo.17083406)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

This repository contains the full source code, data, and manuscript for the research paper titled above, authored by Toshiya Konno. This work is the seventh installment in an evolving series (v2.5–v7.1).

## Overview (v7.1)

Our previous study (v6.0) suggested a "noise-renormalized nonlinear transducer" in a 1D effective model, but that model lacked thermodynamic consistency. This paper addresses this fundamental challenge by detailing the construction of a self-consistent 3D hybrid model where dissipation and fluctuation are rigorously linked by physical laws (Stochastic Projected Gross-Pitaevskii Equation).

Using this physically consistent framework, we report four major findings:
1.  **Universal Gain Suppression:** Confirmed the monotonic suppression of the nonlinear transducer's gain with increasing temperature in 3D, suggesting the universality of this core physical phenomenon.
2.  **Emergent Bistability:** Discovered a temperature-dependent transition from a monostable state to a symmetry-broken "bistable" state in the closed-loop dynamics—an emergent phenomenon unpredictable from lower-dimensional models.
3.  **Alpha Estimation Challenge:** Revealed that the data-driven estimation of the noise-mixing parameter α is fundamentally challenging in this 3D system, providing a physical explanation for this difficulty.
4.  **V-shaped SNR Curve:** Found preliminary evidence of a non-monotonic, V-shaped Signal-to-Noise Ratio (SNR) curve, suggesting a novel cooperative effect between noise and nonlinearity distinct from classical stochastic resonance.

This work establishes the 3D thermal quantum-classical hybrid system as a robust theoretical platform for exploring rich and complex emergent dynamics.

## Repository Contents

This repository is structured to ensure full reproducibility of the results, in line with our "GlassBox" philosophy.

-   **/manuscript:** Contains the full LaTeX source code (`main.tex`), bibliography (`minimal.bib`), and all figure files (`.pdf`) required to compile the final manuscript (v7.1).
-   **/analysis:** Contains all Jupyter notebooks (`.ipynb`) used for simulation, data analysis, and figure generation. The raw data files (`.csv`) generated and used by these notebooks are also included.
-   **/scripts:** (Currently empty) This directory is reserved for build scripts to automate the entire reproduction process.
-   **CITATION.cff:** A machine-readable citation file. Use this to easily cite this work.
-   **README.md:** This file, providing an overview and instructions.

## How to Reproduce the Results

To fully reproduce the findings presented in this paper, please follow these steps:

**Prerequisites:**
-   Git
-   Python 3.8+ (Dependencies are listed in `requirements.txt`)
-   A standard LaTeX distribution (e.g., TeX Live, MiKTeX) with the `latexmk` utility.

**Steps:**

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/k-toppi/CoupledField3D.git
    cd CoupledField3D
    ```

2.  **Set up the Python environment:**
    We recommend using a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Run the analysis and generate figures:**
    The Jupyter notebooks in the `/analysis` directory are numbered in a logical order. Running these notebooks will re-generate the data and figures presented in the paper.

4.  **Recompile the manuscript:**
    Navigate to the `/manuscript` directory and compile the LaTeX source to generate the final PDF.
    ```bash
    cd manuscript
    latexmk -lualatex main.tex
    ```

## Citation

If you use this work in your research, please cite it. This repository includes a `CITATION.cff` file, which can be used with modern citation tools. GitHub will also display a "Cite this repository" button on the main page.

Alternatively, you can use the following reference:

> Konno, T. (2025). *A 3D Mathematical Model of a Dynamically Coupled Field Inspired by Operator Algebras: VII. Thermodynamically Consistent 3D Hybrid Model and Its Emergent Properties* (Version 7.1). Zenodo. https://doi.org/10.5281/zenodo.17083406

## License

This project is licensed under a dual-license model:
-   The source code (including Jupyter notebooks and scripts) is licensed under the **MIT License**.
-   The manuscript text and figures are licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0) License**.

Please see the `LICENSE` and `DATA_LICENSE` files for more details.

## Contact

Toshiya Konno - ktlifeisonlyreallyoverafter60@gmail.com
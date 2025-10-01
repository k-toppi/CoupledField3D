# A 3D Mathematical Model of a Dynamically Coupled Field Inspired by Operator Algebras: VIII. Quantitative Proof of a Finite-Size, Critical-Like Transition

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17217573.svg)](https://doi.org/10.5281/zenodo.17217573)
[![License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY 4.0](https://img.shields.io/badge/Manuscript%20License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)

This repository contains the full source code, data, and manuscript for the research paper titled above, authored by Toshiya Konno. This work is the eighth installment in an evolving series (v2.5-v8.0).

## Overview (v8.0)

Our previous work (v7.1) suggested a temperature-dependent state transition in a 3D hybrid model. This paper provides the definitive **quantitative proof** of this phenomenon. We establish that the system exhibits a **finite-size, critical-like transition** at **T_c ≈ 0.0900**.

### Key Contributions of v8.0:

1.  **Quantitative Proof of Transition:** We demonstrate that three independent thermodynamic indicators (Landau coefficient, susceptibility, order parameter) consistently show singular behavior at the same critical temperature.
2.  **Mechanistic Explanation of Arrhenius Plot:** We reveal that the non-monotonic "hump-shape" of the Arrhenius plot is caused by the temperature-dependent reshaping of the effective potential landscape (a ΔF(T)–prefactor competition).
3.  **Visualization of the Mechanism:** We successfully visualize the transition mechanism, showing a "shallow double-well" at low temperatures (T=0.08) and the vanishing of the central barrier at the critical point (T=0.12).
4.  **Full Reproducibility and Uncertainty Quantification:** All results are supported by robust statistical analyses (Grid Search CV, Moving-Block Bootstrap) and are fully reproducible using the provided code and data.

## Repository Contents

This repository is structured to ensure full reproducibility of the results, in line with our "GlassBox" philosophy.

*   **/manuscript:** Contains the full LaTeX source code (`v8_main.tex`), bibliography (`references.bib`), and all figure files (`.pdf`) required to compile the final manuscript (v8.0).
*   **/analysis:** Contains all Jupyter notebooks (`.ipynb`) used for data analysis and figure generation.
*   **Root Directory:** Contains license files, this README, and other project-wide configuration files.

## How to Reproduce the Results

To fully reproduce the findings presented in this paper, please follow these steps:

**Prerequisites:**

*   Git
*   Python 3.8+ (Dependencies are listed in `requirements.txt`)
*   A standard LaTeX distribution (e.g., TeX Live, MiKTeX) with the `latexmk` utility.

**Steps:**

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/k-toppi/CoupledField3D.git
    cd CoupledField3D
    ```

2.  **Set up the Python environment:** We recommend using a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Run the analysis and generate figures:** The Jupyter notebooks in the `/analysis` directory are numbered in a logical order. Running these notebooks will re-generate the data and figures presented in the paper.
    *   Run `M21_01_Publication_Ready_Figs_v1.ipynb` to generate Fig. 1 and Fig. 2.
    *   Run `A3_01_Analyze_Kramers_Prefactor_v1.ipynb` (v21 Golden Master) to generate Fig. 3.

4.  **Recompile the manuscript:** Navigate to the `/manuscript` directory and compile the LaTeX source to generate the final PDF.
    ```bash
    cd manuscript
    latexmk -lualatex v8_main.tex
    ```

## Citation

If you use this work in your research, please cite it. This repository includes a `CITATION.cff` file, which can be used with modern citation tools. GitHub will also display a "Cite this repository" button on the main page.

Alternatively, you can use the following reference:

> Konno, T. (2025). *A 3D Mathematical Model of a Dynamically Coupled Field Inspired by Operator Algebras: VIII. Quantitative Proof of a Finite-Size, Critical-Like Transition* (Version 8.0). Zenodo. https://doi.org/10.5281/zenodo.17217573

## License

This project is licensed under a dual-license model:
*   The source code (including Jupyter notebooks and scripts) is licensed under the **MIT License**.
*   The manuscript text and figures are licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** License.

Please see the `LICENSE` and `DATA_LICENSE` files for more details.

## Contact

Toshiya Konno - ktlifeisonlyreallyoverafter60@gmail.com
# CoupledField3D

**A 3D Mathematical Model of a Dynamically Coupled Field Inspired by Operator Algebras: IX. Final Determination of the Critical Temperature via a Self-Correcting Process**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17645513.svg)](https://doi.org/10.5281/zenodo.17645513)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

This repository contains the source code, analysis scripts, and manuscript for the research paper titled above, authored by Toshiya Konno. This work is the ninth installment in an evolving series, marking the final determination of the critical temperature ($T_c$).

## Overview (v9.0)

Our previous work (v8.0) provided quantitative proof of a critical-like transition but relied on an absolute-value order parameter, which implicitly assumed perfect symmetry. In this work (v9.0), we overcome this limitation through a **self-correcting approach**. We construct a new analysis pipeline featuring a dynamic reference point ($c^*$) and a robust two-stage estimator for the symmetrization temperature ($T_{\mathrm{sym}}$).

Using this rigorous pipeline and Finite-Size Scaling (FSS) analysis, we have definitively determined the critical temperature to be:
**$T_c = 0.0863 \pm 0.0004$**

## Key Contributions of v9.0:

1.  **Self-Correcting Methodology:** We moved beyond the limitations of v8 by introducing a signed order parameter and a dynamic reference point ($c^*$) to correct for minor asymmetries in the potential.
2.  **Robust $T_{\mathrm{sym}}$ Estimation:** We implemented a two-stage estimator combining Isotonic Regression with a "Bracket Linear" fallback to handle sharp V-shaped $\Delta F$ structures near the critical point (especially at L=160).
3.  **Final Determination of Tc:** Through weighted FSS analysis with $\nu=0.63$, we determined $T_c \approx 0.0863$, demonstrating excellent agreement across system sizes L=100, 128, and 160.
4.  **Full Reproducibility:** All analysis scripts and the final FSS plot generation code are provided to ensure complete reproducibility of the results.

## Repository Contents

This repository is structured to ensure full reproducibility of the results.

*   **/manuscript**: Contains the full LaTeX source code (`v9_manuscript.tex`), bibliography (`references.bib`), and the final PDF (`Konno_Toshiya_CoupledField3D_v9_0.pdf`).
*   **/analysis**: Contains the Python scripts used for the final analysis (`V9_Tsym_Reconciled_Final_v8_3_resilient.py`, `V9_FSS_Plotter.py`) and the result table (`T_sym_table.csv`).
*   **Root Directory**: Contains license files and this README.

> **Note on Data:** Due to file size limitations, the full raw dataset (including large CSV files >25MB) is hosted on Zenodo: **[DOI: 10.5281/zenodo.17645513](https://doi.org/10.5281/zenodo.17645513)**

## How to Reproduce the Results

To fully reproduce the findings presented in this paper, please follow these steps:

### Prerequisites:
*   Python 3.8+ (Required libraries: `numpy`, `pandas`, `scipy`, `matplotlib`, `scikit-learn`)
*   A standard LaTeX distribution (e.g., TeX Live) for compiling the manuscript.

### Steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/k-toppi/CoupledField3D.git
    cd CoupledField3D
    ```

2.  **Download Raw Data:**
    Download the raw CSV files (e.g., `V9_PT_... .csv`) from the Zenodo repository linked above and place them in the `/analysis` directory (or a directory of your choice).

3.  **Run the Analysis (T_sym Extraction):**
    Use the resilient script to extract $T_{\mathrm{sym}}$ for each system size.
    ```bash
    python analysis/V9_Tsym_Reconciled_Final_v8_3_resilient.py --data_dir [path_to_csvs] ...
    ```
    *(Note: See the script header or paper Methods for specific arguments used for each L)*

4.  **Generate FSS Plot and Tc:**
    Run the plotter script to perform FSS and generate the final figure.
    ```bash
    python analysis/V9_FSS_Plotter.py
    ```
    This will output `FSS_Final_Plot.pdf` and print the final $T_c$ value.

## Citation

If you use this work in your research, please cite it.

**Konno, T. (2025).** *A 3D Mathematical Model of a Dynamically Coupled Field Inspired by Operator Algebras: IX. Final Determination of the Critical Temperature via a Self-Correcting Process.* Zenodo. [https://doi.org/10.5281/zenodo.17645513](https://doi.org/10.5281/zenodo.17645513)

## License

This project is licensed under a dual-license model:

*   The source code (including Python scripts) is licensed under the **MIT License**.
*   The manuscript text and figures are licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0) License**.

Please see the `LICENSE` and `DATA_LICENSE` files for more details.

## Contact

Toshiya Konno - ktlifeisonlyreallyoverafter60@gmail.com

---

## Latest manuscript: Part X

**Title**  
*A 3D Mathematical Model of a Dynamically Coupled Field Inspired by Operator Algebras: X. Effective-Temperature Mapping of ATP-Scale Energy Input and Ordered-Side Transport in a Hybrid Model*

**Summary**  
This part investigates how an ATP-based effective-temperature mapping may influence energy propagation under strong thermal noise within the 3D quantum-classical hybrid model developed in this project. Using the critical-temperature estimate obtained in Part IX as a reference, the manuscript introduces an effective temperature based on the in vivo free-energy scale of ATP hydrolysis and compares a low-noise ATP-scale regime with a high-noise reference regime.

**Main points**
- Introduces an ATP-scale effective-temperature mapping with $T_{\mathrm{eff}} \approx 0.0534$
- Compares pulse propagation at $T=0.0534$ and $T=0.10$
- Interprets the results within a finite-size $L=100$ setting
- Explicitly distinguishes effective energy-scale mapping from a direct microscopic ATP-hydrolysis model
- Includes limitations, finite-size caveats, and pre-crash-window interpretation

**Reproducibility**
The main figures in Part X were generated using:
- `V10_Generate_Figures_1_and_2_v6.py`

All scripts, data, and manuscript sources are included in this repository.

**Zenodo archive**
Official archived version: DOI: [10.5281/zenodo.18975719](https://doi.org/10.5281/zenodo.18975719)

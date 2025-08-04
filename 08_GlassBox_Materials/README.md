# A 3D Mathematical Model of a Dynamically Coupled Field (Version 5.0)

This repository contains the full source code, data, and supplementary materials for the paper "A 3D Mathematical Model of a Dynamically Coupled Field Inspired by Operator Algebras" by Toshiya Konno.

## Abstract

In our previous work (Version 4.0), we introduced thermal fluctuations into our 3D mathematical model of a dynamically coupled quantum-classical system, revealing a novel "Thermally Excited Oscillatory State" (TEOS) and strong indications of stochastic resonance (SR). This paper builds directly upon that foundation, presenting a rigorous quantitative and theoretical analysis of the system's rich phenomenology. Through extensive numerical simulations, performing a large number of runs to ensure statistical reliability, we quantitatively demonstrate the existence of SR by analyzing the signal-to-noise ratio (SNR), identifying an optimal noise intensity that maximizes signal amplification. Furthermore, we show the universality of this phenomenon across a range of dissipation strengths, providing new insights into the interplay between dissipation and the effectiveness of SR. Complementing these numerical results, we develop a theoretical framework based on linear stability analysis. This framework explains the structure of the system's phase diagram—comprising the stable coupled, pinned, and TEOS phases—by deriving the critical conditions for phase transitions from first principles. These combined findings not only solidify the physical relevance of our model but also provide a deeper, mechanistic understanding of how complex systems can harness noise for robust information transport, offering a potential physical framework for understanding robust information transport in complex, noisy environments. These mechanisms are akin to those found in intracellular processes.

## Reproducibility

This project is designed to be fully reproducible. The entire toolchain, from raw simulation to final figure generation, is automated via Python scripts.

### Quickstart

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YourGitHubUsername/CoupledField3D.git
    cd CoupledField3D/08_GlassBox_Materials
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run all simulations:** (This will take several hours)
    ```bash
    python run_all_simulations.py
    ```

4.  **Plot all figures:**
    ```bash
    python plot_all_figures.py
    ```
    The reproduced figures will be saved in the `01_Figures_Reproduced` directory.

## The "Glass Box" Approach: Transparency in AI-Human Collaboration

This research represents a test case for a new model of scientific discovery, leveraging a deep, collaborative partnership between a human researcher and an advanced AI. To ensure full transparency and address the "black box" problem, we provide the following materials in this repository:

*   **/prompts:** Key dialogues with the AI that led to major breakthroughs in the model.
*   **Validation_Notebook.ipynb:** A minimal, executable notebook demonstrating our core validation logic (SNR calculation, stability analysis).
*   **Automated Scripts:** The `run_all_simulations.py` and `plot_all_figures.py` scripts, which form a fully automated and verifiable pipeline from code to final results.

### A Note on Evaluation Criteria

We propose that this work, as a product of AI-Human collaboration, should be evaluated on three axes:
1.  **Reproducibility:** The ease with which a third party can reproduce all results using the provided code and parameters.
2.  **Verifiability:** The clarity of the automated tests (e.g., conservation laws, statistical significance) that validate the model's outputs.
3.  **Extensibility:** The degree to which the provided prompts and metadata, under a permissive license (CC-BY), allow others to build upon this work.

## How to Cite

If you use this model or the associated code in your research, please use the citation information provided in the `CITATION.cff` file.
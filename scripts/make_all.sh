#!/bin/bash
# ==============================================================================
#   Build Script for Reproducing the Manuscript PDF
# ==============================================================================
#
#   This script automates the recompilation of the manuscript from its
#   LaTeX source files.
#
#   Usage:
#   From the root directory of the repository (CoupledField3D-main), run:
#   bash scripts/make_all.sh
#
# ==============================================================================

# Exit immediately if a command exits with a non-zero status.
set -e

echo "==> Starting manuscript build process..."

# Navigate to the manuscript directory.
# The script assumes it is run from the repository's root directory.
cd manuscript

# Check if the main LaTeX file exists
if [ ! -f main.tex ]; then
    echo "Error: main.tex not found in manuscript/ directory."
    exit 1
fi

echo "==> Found main.tex. Compiling with lualatex via latexmk..."

# Compile the LaTeX source to generate the PDF.
# latexmk is a robust script that handles multiple compilations for references, etc.
latexmk -lualatex main.tex

echo "==> Build process completed successfully."
echo "==> The final PDF can be found at: manuscript/main.pdf"

# Navigate back to the root directory
cd ..

exit 0
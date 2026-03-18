# MACR

[![Tests](https://github.com/cda24/MACR/actions/workflows/tests.yml/badge.svg)](https://github.com/cda24/MACR/actions)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

A simple Python project using pytest.
**MACR** (pronounced _maker_) - The Material Attenuation Calculator for Radiation - is a python library to quickly generate interaction cross-sections of any material for protons (NIST PSTAR and SRIM), electrons (NIST ESTAR), and x-rays (NIST XCOM).

It contains a database of cross-sections for each element, which are then combined according to their atomic weight to provide cross-sections for materials and compounds. The library can be used to the transmission and absorption through multiple layers of different materials in a one-dimensional configuration (two-dimensional is an ongoing project).

## Installation

For the source code of examples and the verification notebooks please clone the git repository and pip install locally:

1. Clone the repository:

    ```bash
    git clone https://github.com/cda24/MACR.git 
    ```

2. Install the package:

    ```bash
    pip install -e .
    ```

> Requirements in pyproject.toml

## References 
The primary references should be to the relevant material databases:

```
@article{berger2010xcom,
  title={XCOM: photon cross sections database},
  author={Berger, MJOK},
  journal={http://www.nist.gov/pml/data/xcom/index.cfm},
  year={2010}
}
```
```
@article{berger1992estar,
  title={ESTAR, PSTAR, and ASTAR: Computer programs for calculating stopping-power and range tables for electrons, protons, and helium ions},
  author={Berger, Martin J},
  journal={Unknown},
  year={1992}
}
```
```
@article{ziegler2010srim,
  title={SRIM--The stopping and range of ions in matter (2010)},
  author={Ziegler, James F and Ziegler, Matthias D and Biersack, Jochen P},
  journal={Nuclear Instruments and Methods in Physics Research Section B: Beam Interactions with Materials and Atoms},
  volume={268},
  number={11-12},
  pages={1818--1823},
  year={2010},
  publisher={Elsevier}
}
```

## Authors

MACR is developed by:

- **Dr C. D. Armstrong**
- J. K. Patel
- A. Brainthra

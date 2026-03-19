# MACR

[![Tests](https://github.com/cda24/MACR/actions/workflows/tests.yml/badge.svg)](https://github.com/cda24/MACR/actions)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

**MACR** (pronounced _maker_) - The Material Attenuation Calculator for Radiation - is a python library to generate interaction cross-sections of any material for protons (NIST PSTAR and SRIM), electrons (NIST ESTAR), and x-rays (NIST XCOM).

It contains a database of cross-sections for each element, which are then combined according to their atomic weight to provide cross-sections for materials and compounds. The library can be used to the transmission and absorption through multiple layers of different materials.

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

## Description

MACR is structured as follows:
* `Engine` is the backend class that interacts directly with the cross-section database to create new materials and cross-sections on demand. Using solely the engine allows the user to interrogate the contents of the database and not much else.
* `Material` class utilises the `engine` and generates an object with a fixed density and set of energies to consider. Using solely the `material` allows users to determine the cross-sections as a function of energy - similar to NIST XCOM, generate the transmission/absorption functions for a set length - similar to CRXO, and/or calculate the deposition profile - similar to SRIM.
* `Layer` class is then built upon the Material class to wrap a single material with a defined thickness, layers are also defined as _active_ or not as a flag to determine if these layers can be used to detect radiation. 
* `System` class is built from `Layers` (or directly from `Materials` although this is more cumbersome) to define a series or areal pattern of filters and active layers. This class makes it simple to generate response matrices for both linear and areal absorption spectromters. Both for RCF stacks with proton deposition and x-ray spectrometers can be constructed in MACR.


Helper tools for ROI analysis of images, and direct unfolding from measurements are in development. 

## Simple Use Cases
#### Loading Elemental Cross-Sections
```python
from macr.material import Material
import matplotlib.pyplot as plt 

Al = Material(materialstr='Al',density=2.71)

plt.plot(Al.energies,Al.sigma)
plt.ylabel('Cross-section (g/cc)')
plt.xlabel('Energy (MeV)')
```

#### Overriding default energies
```python
import numpy as np 

energies = np.linspace(0.01,1,100) #MeV
Al = Material(materialstr='Al',density=2.71,energies=energies)
```

#### Custom material transmission
```python
import numpy as np 

energies = np.linspace(0.01,1,100) #MeV
CsI = Material(materialstr='CsI',density=4.51,energies=energies)

plt.plot(energies,CsI.get_transmission(1),label='Transmitted through 1 mm')
plt.plot(energies,CsI.get_absorption(1),label='Absorbed in 1 mm')
```

#### Defining Layers
Common materials are predefined in the configured library so for simplicity we can load them directly and create a layers of _passive_ Al and _active_ CsI

```python
from macr.library import Al,CsI
from macr.system import Layer

l1 = Layer(Al,0.1,active=False)
l2 = Layer(CsI,0.1,active=True)
```

Layers retain the material methods so the prior example becomes:

```python
plt.plot(l1.energies,l1.get_transmission(1),label='Transmitted through L1')
plt.plot(l2.energies,l2.get_absorption(1),label='Absorbed in L2')
```

However the layers currently don't know about each other and so we see absorption in the CsI that is non-physical. To solve that we introduce Systems

#### Creating a system 

```python
from macr.system import System

s1 = System()
s1.add_layer(l1)
s1.add_layer(l2)
s1.generate_response()
s1.plot_response()
```


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

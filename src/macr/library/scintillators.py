"""Predefined scintillator materials.

Each exported symbol is a :class:`macr.material.Scintillator` configured with a compound composition, density, and conversion factor.
"""

from ..material import Scintillator
from ..library import ENERGIES, ENGINE

# region - Scintillators
_anthracene_constant = 16
ANTHRACENE = Scintillator(
    "C14H10",
    1.283,
    generic_name="ANTHRACENE",
    energies=ENERGIES,
    engine=ENGINE,
    kappa=_anthracene_constant,
)
GADOX = Scintillator(
    "Gd2O2S", 7.44, generic_name="Gadox", energies=ENERGIES, engine=ENGINE, kappa=60
)
LANEX = Scintillator(
    "Gd2O2S", 7.44, generic_name="Lanex", energies=ENERGIES, engine=ENGINE, kappa=60
)
LSO = Scintillator(
    "Lu2SiO5", 7.4, generic_name="LSO", energies=ENERGIES, engine=ENGINE, kappa=30
)
LYSO = Scintillator(
    "Lu1.8Y0.2SiO5",
    7.15,
    generic_name="LYSO",
    energies=ENERGIES,
    engine=ENGINE,
    kappa=25,
)
LuAG = Scintillator(
    "Lu3Al5O12", 6.3, generic_name="LuAG", energies=ENERGIES, engine=ENGINE, kappa=25
)
BGO = Scintillator(
    "Bi4Ge3O12", 7.13, generic_name="BGO", energies=ENERGIES, engine=ENGINE, kappa=9
)
YAG = Scintillator(
    "Y3Al5O12", 4.55, generic_name="YAG", energies=ENERGIES, engine=ENGINE, kappa=35
)
CsI = Scintillator(
    "CsI", 4.51, generic_name="CsI", energies=ENERGIES, engine=ENGINE, kappa=54
)
CH = Scintillator(
    "C8H8",
    1.06,
    generic_name="CH",
    energies=ENERGIES,
    engine=ENGINE,
    kappa=0.56 * _anthracene_constant,
)
# endregion - Scintillators

"""Predefined radiochromic film (RCF) layer systems.

Layer thicknesses are expressed in millimetres, and active layers are marked for response matrix generation.
"""

from ..material import Material, Scintillator
from ..system import Layer, System
from ..library import ENERGIES, ENGINE

# region - RCF
basePolyester = Material(
    "C10H8O4", density=1.397,  energies=ENERGIES, engine=ENGINE, generic_name="BaseLayer"
)
activeLayer = Material(
    "C2H4O1", density=1.2,  energies=ENERGIES, engine=ENGINE, generic_name="ActiveLayer"
)
acrylicAdhesive = Material(
    "C7H12O2", density=1.2,  energies=ENERGIES, engine=ENGINE, generic_name="BaseLayer"
)

"""Reference: http://www.gafchromic.com/documents/EBTXD_Specifications_Final.pdf"""
EBT_XD = System(
    [
        Layer(basePolyester, 0.125, 0),
        Layer(activeLayer, 0.025, 1),
        Layer(basePolyester, 0.125, 0),
    ]
)
"""Reference: http://www.gafchromic.com/documents/gafchromic-hdv2.pdf"""
HD_V2 = System([Layer(activeLayer, 0.012, 1), Layer(basePolyester, 0.097, 0)])

"""Reference: http://www.gafchromic.com/documents/EBT3_Specifications.pdf"""
EBT_V3 = System(
    [
        Layer(basePolyester, 0.125, 0),
        Layer(activeLayer, 0.028, 1),
        Layer(basePolyester, 0.125, 0),
    ]
)

"""References:

* http://www.gafchromic.com/documents/PC-11805_Gafchromic_XR.pdf
* https://ijrr.com/article-1-1720-en.pdf
"""
XR_RV3 = System(
    [
        Layer(basePolyester, 0.097, 0),
        Layer(acrylicAdhesive, 0.020, 0),
        Layer(activeLayer, 0.017, 1),
        Layer(basePolyester, 0.097, 0),
    ]
)
# endregion - RCF

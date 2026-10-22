"""Predefined imaging-plate (IP) detector systems.

The exported systems represent commercially used imaging-plate layer
constructions. Layer thicknesses are expressed in millimetres.
"""

from ..material import Material
from ..system import Layer, System
from .rcf import basePolyester
from ..library import ENERGIES, ENGINE

# region - IP
activeIPSR = Material(
    "BaFBr", density=3.07,  energies=ENERGIES, engine=ENGINE, generic_name="ActiveIPSR"
)
activeIPTR = Material(
    "BaFBr0.85I0.15", density=2.61,  energies=ENERGIES, engine=ENGINE, generic_name="ActiveIPTR"
)
activeIPMS = Material(
    "BaFBr0.85I0.15", density=3.18,  energies=ENERGIES, engine=ENGINE, generic_name="ActiveIPMS"
)

"""Reference: https://pubs.aip.org/aip/rsi/article/79/11/113102/351195/Evaluation-of-the-sensitivity-and-fading"""

IP_MS = System(
    [
        Layer(basePolyester, 0.008, 0),
        Layer(activeIPMS, 0.124, 1),
        Layer(basePolyester, 0.300, 0),
    ]
)

IP_SR = System(
    [
        Layer(basePolyester, 0.009, 0),
        Layer(activeIPSR, 0.112, 1),
        Layer(basePolyester, 0.300, 0),
    ]
)

IP_TR = System(
    [
        Layer(activeIPTR, 0.060, 1),
        Layer(basePolyester, 0.300, 0),
    ]
)
# endregion - IP

"""Predefined materials, detector systems, and shared library settings.

The library exposes ready-to-use :class:`macr.material.Material`,
:class:`macr.material.Scintillator`, and :class:`macr.system.System` objects.
The shared :data:`ENERGIES` grid and :data:`ENGINE` instance are used when
constructing these objects and can be replaced before importing a submodule
that depends on them.
"""

import numpy as np
from ..engine import Engine

# Declarations used by the predefined library objects.
ENERGIES = np.geomspace(0.01, 1, 10000)
ENGINE = Engine("NIST")  # feature complete, changes to other engines might cause errors

from . import elements as elements
from . import g4nist as g4nist
from . import rcf as rcf
from . import scintillators as scintillators
from . import ip as ip

# for those who want access to everything without importing each submodule
from .elements import *
from .g4nist import *
from .rcf import *
from .scintillators import *
from .ip import *
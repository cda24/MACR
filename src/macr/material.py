import numpy as np
import re
from .engine import Engine


class Material:
    """
    Material Class for pyNIST Library

    Computes the necessary cross-sections from the defined database for any arbitary
    material composition. Materials should be declared as camel-case elements such as
    "SiO2" or "Al" for Quartz and elemental Aluminium respectively

    Warning: Lowercase element names are ignored.

    Intialisation Parameters
    ----------
    material - str - Chemical composition of material
    density - float - g/cc
    energies - array or None - array of desired energies in MeV if undeclared uses database defaults
    engine - str or Engine - Engine declaration must be type: "str" or "Engine"
                             For most efficient use pass pre-loaded Engine class (about 2x as fast)


    Functions
    ---------

    Automatic - Happens during Initialisation:
        generateCrossSections - sets cross-section (sigma) and energies corresponding to the material
    Manual - Called by user:
        get_transmission - calculates the transmission through material for thickness in mm
        get_absorption - calculates the absorption in material for thickness in mm

    """

    def __init__(
        self, material, density, energies=None, engine="NIST", genericName=None
    ):
        # initialise or use engine
        assert (isinstance(engine, str)) or (isinstance(engine, Engine))

        self.set_engine(engine)

        self.material = self.engine.parse_formula(material)
        self.density = density

        ## handle energies = None case
        # load energies of first element to use as base

        if energies is None:
            energies, _ = self.engine.db_scraper(list(self.material.keys())[0])

        self.update_cross_sections(energies)

        if genericName is None:
            self.materialstr = material
        else:
            assert isinstance(genericName, str)
            self.materialstr = genericName

    def _parse_compound(self, compound):
        element_pat = re.compile(r"([A-Z][a-z]?)(\d*)")
        return element_pat.findall(compound)

    def update_cross_sections(self, energies):
        x = self.engine.db["atomic"]
        sigma = np.zeros_like(energies)
        total_weight = 0
        for key, value in self.material.items():
            total_weight += value * x[x["Symbol"] == key]["Weight"].to_numpy()[0]

        for key, value in self.material.items():
            e, c = self.engine.db_scraper(key, energies)
            fractional_weight = (
                value * x[x["Symbol"] == key]["Weight"].to_numpy()[0]
            ) / total_weight
            sigma[:] += c * fractional_weight

        self.energies = energies
        self.sigma = sigma
        if (
            (self.engine.name == "ESTAR")
            or (self.engine.name == "PSTAR")
            or (self.engine.name == "SRIM")
        ):
            self._estarcorrection()

    def _estarcorrection(self):
        """correction for the estar units"""
        self.sigma = self.sigma / self.energies

    def get_transmission(self, thickness):
        """calculates the transmission of x-rays through a layer:
        * thickness must be in mm"""
        return np.exp(-self.sigma * self.density * (thickness * 0.1))

    def get_absorption(self, thickness):
        """calculates the absorption of x-rays through a layer:
        * thickness must be in mm"""
        return 1 - self.get_transmission(thickness)

    def get_profile(self, thickness, nstep=1000):
        """
        Returns the z profile deposition for radiation transmitting through
        Thickness in mm, nstep is number of elements calculated
        By default this is 1000 so the resolution is thickness/nstep.

        Solved for the full array, particles are tracked until they run out of energy

        """
        # initialise seed energies
        hold_energies = self.energies
        # initialise arrays
        track_map = np.zeros((len(self.energies), nstep))
        energy_map = np.zeros((len(self.energies), nstep))

        # set initial energy
        energy_map[:, 0] = self.energies

        # initialise output
        self.output = {
            "energies": self.energies,
        }

        for n in range(1, nstep):
            track = self.get_absorption(thickness / nstep) * self.energies
            delta_e = self.get_transmission(thickness / nstep) * self.energies
            self.energies = np.clip(delta_e, 0, None)
            self.update_cross_sections(self.energies)

            ## update arrays
            energy_map[:, n] = self.energies
            track_map[:, n] = track

        # generate step positions for plotting
        zsteps = np.linspace(0, thickness, nstep)

        # reset material database:
        self.update_cross_sections(hold_energies)

        self.output["energy_map"] = energy_map
        self.output["track_map"] = track_map
        self.output["zsteps"] = zsteps

    def set_engine(self, engine):
        if isinstance(engine, str):
            self.engine = Engine(engine)
        else:
            self.engine = engine

    # depreciating functions
    def generateCrossSections(self, material, energies):
        self.update_cross_sections(energies)

    def regenerateCrossSections(self):
        self.update_cross_sections(self.energies)


class Scintillator(Material):
    def __init__(
        self,
        material,
        density,
        kappa=1.0,
        energies=None,
        engine="NIST",
        genericName=None,
    ):
        super().__init__(material, density, energies, engine, genericName)
        self.kappa = kappa

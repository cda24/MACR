import numpy as np
import re
from .engine import Engine


class Material:
    """Calculate attenuation for a material composition.

    Parameters
    ----------
    material : str
        Chemical formula, such as ``"SiO2"`` or ``"Al"``.
    density : float
        Material density in g/cm³.
    energies : array-like or None, optional
        Energy values in MeV. Database energies are used when omitted.
    engine : str or Engine, default="NIST"
        Database engine name or an already initialised :class:`Engine`.
    generic_name : str or None, optional
        Display name used when the material is shown in a system.
    """

    def __init__(
        self, material, density, energies=None, engine="NIST", generic_name=None
    ) -> None:
        # initialise or use engine
        assert (isinstance(engine, str)) or (isinstance(engine, Engine))

        if isinstance(engine, str):
            self.engine = Engine(engine)
        else:
            self.engine = engine

        self.material = self.engine.parse_formula(material)
        self.density = density

        ## handle energies = None case
        # load energies of first element to use as base

        if energies is None:
            energies, _ = self.engine.db_scraper(list(self.material.keys())[0])

        self.update_cross_sections(energies)

        if generic_name is None:
            self.materialstr = material
        else:
            assert isinstance(generic_name, str)
            self.materialstr = generic_name

    def update_cross_sections(self, energies):
        """Recalculate cross-sections at the specified energies.

        Parameters
        ----------
        energies : array-like
            Energy values in MeV.
        """
        x = self.engine.database.atomic
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

    def get_transmission(self, thickness) -> np.ndarray:
        """Calculate transmission through a layer.

        Parameters
        ----------
        thickness : float
            Layer thickness in mm.

        Returns
        -------
        numpy.ndarray
            Transmitted fraction at each energy.
        """
        return np.exp(-self.sigma * self.density * (thickness * 0.1))

    def get_absorption(self, thickness) -> np.ndarray:
        """Calculate absorption through a layer.

        Parameters
        ----------
        thickness : float
            Layer thickness in mm.

        Returns
        -------
        numpy.ndarray
            Absorbed fraction at each energy.
        """
        return 1 - self.get_transmission(thickness)

    def get_profile(self, thickness, nstep=1000) -> None:
        """Calculate the z profile deposition for radiation transmitting through.

        Parameters
        ----------
        thickness : float
            Material thickness in mm.
        nstep : int, default=1000
            Number of elements calculated. By default this is 1000 so the resolution is thickness/nstep.

        Notes
        -----
        Solved for the full array, particles are tracked until they run out of energy

        Results are stored in :attr:`output` with ``energy_map``, ``track_map``, and ``zsteps`` entries.
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

    def _estarcorrection(self):
        """Apply the unit correction required by ESTAR, PSTAR, and SRIM."""
        self.sigma = self.sigma / self.energies

    def _parse_compound(self, compound):
        element_pat = re.compile(r"([A-Z][a-z]?)(\d*)")
        return element_pat.findall(compound)

    # depreciating functions
    def generateCrossSections(self, material, energies):
        """Deprecated alias for :meth:`update_cross_sections`."""
        self.update_cross_sections(energies)

    def regenerateCrossSections(self):
        """Deprecated alias for :meth:`update_cross_sections`."""
        self.update_cross_sections(self.energies)

class Scintillator(Material):
    """Material with a scintillator response scaling factor.

    Parameters
    ----------
    material : str
        Chemical formula.
    density : float
        Material density in g/cm³.
    kappa : float, default=1.0
        Scintillator scaling factor from energy deposition to counts.
    energies : array-like or None, optional
        Energy values in MeV.
    engine : str or Engine, default="NIST"
        Database engine name or an initialised engine.
    generic_name : str or None, optional
        Display name for the material.
    """

    def __init__(
        self,
        material,
        density,
        kappa=1.0,
        energies=None,
        engine="NIST",
        generic_name=None,
    ) -> None:
        super().__init__(material, density, energies, engine, generic_name)
        self.kappa = kappa

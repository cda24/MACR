from dataclasses import dataclass, field
from typing import ArrayLike, List
from abc import ABC, abstractmethod
import numpy as np
import copy
from scipy.interpolate import interp1d


@dataclass
class Spectra(ABC):
    """
    Abstract base class for spectral definitions.

    Defines common interface for different spectral types with shared variables
    and methods for generation, normalization, and analysis.
    """

    energies: ArrayLike
    spectra: ArrayLike = field(default=None)
    parameters: List[float] = field(default_factory=list)
    name: str = "Spectrum"

    def __post_init__(self):
        """Validate and convert inputs to numpy arrays."""
        self.energies = np.asarray(self.energies)

        if self.spectra is not None:
            self.spectra = np.asarray(self.spectra)
            if len(self.energies) != len(self.spectra):
                raise ValueError(
                    f"energies and spectra must have same length. "
                    f"Got {len(self.energies)} and {len(self.spectra)}"
                )

        ## Preserve initialisation energies
        self._energies = copy.copy(self.energies)
        self._spectra = copy.copy(self.spectra)

    ## Preserve initialisation energies
    _energies: ArrayLike
    _spectra: ArrayLike

    @abstractmethod
    def generate(self) -> np.ndarray:
        """
        Generate spectral values from energies and parameters.
        Must be implemented by subclasses.

        Returns
        -------
        np.ndarray
            Generated spectral values
        """
        pass

    def update_parameters(self, new_parameters: List[float]) -> None:
        """
        Update spectrum parameters and regenerate spectrum.

        Parameters
        ----------
        new_parameters : list
            New parameter values
        """
        self.parameters = list(new_parameters)
        self.spectra = self.generate()

    def interpolate(self, new_energies: ArrayLike) -> np.ndarray:
        """
        Interpolate spectrum to new energy grid.

        Parameters
        ----------
        new_energies : ArrayLike
            New energy grid

        Returns
        -------
        np.ndarray
            Interpolated spectral values
        """
        if self.spectra is None:
            raise ValueError("Spectrum must be generated before interpolation")

        f = interp1d(
            self.energies, self.spectra, kind="cubic", bounds_error=False, fill_value=0
        )

        return f(new_energies)

    def _normalise_counts(self):
        self.spectra = self._spectra / np.trapezoid(self._spectra)

    def _normalise_energies(self):
        self.spectra = self._spectra / np.trapezoid(self._spectra, x=self._energies)

    def _revert(self):
        self.energies = copy.copy(self._energies)
        self.spectra = copy.copy(self._spectra)

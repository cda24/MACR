import numpy as np
from scipy.interpolate import pchip
import pandas as pd
import glob
import re
from pathlib import Path
from enum import IntEnum
from dataclasses import dataclass
from typing import Final, Literal

# Resolve the path to the root of the project
ROOT_DIR = Path(__file__).resolve().parents[0]  # Goes from engine.py -> database

# Now get path to the database directory
DATABASE_DIR = ROOT_DIR / "database"

AVAILABLE_DATABASES: Final[frozenset[str]] = frozenset(
    {"NIST", "ESTAR", "PSTAR", "SRIM"}
)

class NISTColumn(IntEnum):
    """Available NIST XCOM cross-section columns."""

    COHERENT_SCATTER = 1
    INCOHERENT_SCATTER = 2
    PHOTOELECTRIC_ABSORPTION = 3
    NUCLEAR_PAIR_PRODUCTION = 4
    ELECTRONIC_PAIR_PRODUCTION = 5
    TOTAL = 6

class ESTARColumn(IntEnum):
    """Available NIST ESTAR stopping-power columns."""

    COLLISIONAL = 1
    RADIATIVE = 2
    TOTAL = 3

class PSTARColumn(IntEnum):
    """Available NIST PSTAR stopping-power columns."""

    COLLISIONAL = 1
    RADIATIVE = 2
    TOTAL = 3

class SRIMColumn(IntEnum):
    """Available SRIM stopping-power columns."""

    ELECTRONIC = 1
    NUCLEAR = 2
    TOTAL = 3

@dataclass(frozen=True)
class EngineConfig:
    """Configuration required to read one cross-section database."""

    skip_rows: int
    default_column: int
    avail_columns: IntEnum
    warning: str | None = None

ENGINE_CONFIGS: dict[str, EngineConfig] = {
    "NIST": EngineConfig(
        skip_rows=3,
        default_column=NISTColumn.TOTAL,
        avail_columns=NISTColumn
        
    ),
    "ESTAR": EngineConfig(
        skip_rows=8,
        default_column=ESTARColumn.TOTAL,
        avail_columns=ESTARColumn,
        warning="ESTAR database incomplete, please consider pushing update to repo",
    ),
    "PSTAR": EngineConfig(
        skip_rows=8,
        default_column=PSTARColumn.TOTAL,
        avail_columns=PSTARColumn,
        warning="PSTAR database incomplete, please consider SRIM engine instead",
    ),
    "SRIM": EngineConfig(
        skip_rows=25, 
        default_column=SRIMColumn.TOTAL,
        avail_columns=SRIMColumn
    ),
}

@dataclass
class EngineDatabase:
    """Atomic metadata and material names loaded for an engine."""

    atomic: pd.DataFrame
    material_list: list[str]


class Engine:
    """
    Handles the communication to the local database of elements for the `Material` classes
    This can be pre-loaded for efficient operation but is otherwise unnecessary for end users as `Material` can load engine on demand.

    Parameters
    ----------
    name : {"NIST", "ESTAR", "PSTAR", "SRIM"}
        Database to use for cross-section data.

    Notes
    -----
    Element symbols in chemical formulas must use their conventional capitalisation.
    """

    def __init__(self, name: Literal["NIST", "ESTAR", "PSTAR", "SRIM"]) -> None:
        assert name in AVAILABLE_DATABASES, (
            f"Invalid engine name: {name}. Must be one of {AVAILABLE_DATABASES}."
        )

        config: EngineConfig = ENGINE_CONFIGS[name]
        
        self.name: str = name
        self.db_path: str = f"{DATABASE_DIR}/{self.name}/"

        # set Interpolation Method - can be reconfigured if desired but pchip worked best under testing
        self._interpolation_method = pchip

        self.database = EngineDatabase(
            atomic=self._generate_atomic_table(),
            material_list=self._generate_material_list(),
        )
        
        self.skip_rows: int = config.skip_rows
        self.col: int = config.default_column
        if config.warning:
            print(config.warning)

    def parse_formula(self, formula: str) -> dict[str, float]:
        """Parse a chemical formula into element counts.

        Parameters
        ----------
        formula : str
            Chemical formula, such as ``"SiO2"`` or ``"BaFBr0.85"``.

        Returns
        -------
        dict[str, float]
            Mapping from element symbols to their counts.
        """
        # Initialize a dictionary to store the element counts
        element_counts = {}

        # Use a regular expression to match elements and counts in the formula
        elements = re.findall(r"([A-Z][a-z]*|[A-Z])([0-9]*\.?[0-9]*)", formula)

        # Iterate over the elements and counts in the formula
        for element, count in elements:
            # If the element is not in the element_counts dictionary, add it with a count of 0
            if element not in element_counts:
                element_counts[element] = 0

            # If the count is not empty, add it to the count for the element
            if count:
                element_counts[element] += float(count)
            # If the count is empty, increment the count for the element by 1
            else:
                element_counts[element] += float(1)

        # Return the element counts dictionary
        return element_counts

    def missing_atomic_entries(self) -> list[str]:
        """Return atomic symbols without corresponding material files.

        Returns
        -------
        list[str]
            Sorted symbols present in the atomic database but absent from the selected cross-section database.
        """
        atomic_symbols = set(self.database.atomic["Symbol"].astype(str).tolist())
        missing = sorted(list(atomic_symbols - self._materials))
        return missing

    def list_available_columns(self) -> None:
        """Print the cross-section columns available for this engine. (based on the loaded database)"""
        for e in ENGINE_CONFIGS[self.name].avail_columns:
            print(f"{e.name}: {e.value}")

    def change_column(self, new_col: int) -> None:
        """Select the cross-section column read by :meth:`db_scraper`.
        Use method :meth:`list_available_columns` to see valid columns for the current engine.

        Parameters
        ----------
        new_col : int
            Valid column number for the configured database. The corresponding column enum, such as :class:`NISTColumn`, may be used.

        Raises
        ------
        ValueError
            If ``new_col`` is not available for this engine.

        Examples
        -----
        >>> engine = Engine("NIST")
        >>> engine.change_column(NISTColumn.COHERENT_SCATTER)
        """
        # Check if the new column is valid for the current engine
        if new_col not in [e.value for e in ENGINE_CONFIGS[self.name].avail_columns]:
            raise ValueError(
                f"Invalid column {new_col} for engine {self.name}. Use list_available_columns() to see valid columns."
            )
        self.col = new_col
        print(f"Column changed to {ENGINE_CONFIGS[self.name].avail_columns(new_col).name} ({new_col}) for engine {self.name}.")

    def db_scraper(self, material, energies=None) -> tuple[np.ndarray, np.ndarray]:
        """Load and optionally interpolate cross-sections for a material.

        Parameters
        ----------
        material : str
            Element or material name present in the selected database.
        energies : array-like or None, optional
            Energies in MeV at which to interpolate the cross-section. If
            ``None``, return the database energies.

        Returns
        -------
        tuple[numpy.ndarray, numpy.ndarray]
            Energy values and corresponding cross-sections.
        """
        assert material in self._materials, (
            f"{material} not present in {self.name} database consider updating repository"
        )

        if material.lower() == "vac":
            assert energies is not None, print(
                "Energies must be defined for vacuum transmission"
            )
            return energies, np.ones(len(energies))
        else:
            match self.name:
                case "SRIM":
                    # print('loading from SRIM')
                    # units conversion for SRIM
                    units = {
                        "eV": 1e-6,
                        "keV": 1e-3,
                        "MeV": 1,
                        "GeV": 1e3,
                    }
                    # by column operators
                    conv = {
                        0: lambda x: x,
                        1: lambda x: units[x[-4:]],
                        2: lambda x: float(x) * 1000,
                        3: lambda x: float(x) * 1000,
                    }

                    data = np.loadtxt(
                        f"{self.db_path}{self.name}_{material}.txt",
                        skiprows=25,
                        max_rows=150,
                        converters=conv,
                        usecols=[0, 1, 2, 3],
                    )

                    e_list = self._nonuniquer(
                        np.array(data[:, 0]) * np.array(data[:, 1])
                    )

                    match self.col:
                        case 1:
                            # Returns only electronic cross-section
                            c_list = np.array(data[:, 1])
                        case 2:
                            # Returns only nuclear cross-section
                            c_list = np.array(data[:, 2])
                        case 3:
                            # Returns summation of both (default)
                            c_list = np.array(data[:, 1]) + np.array(data[:, 2])

                    if energies is not None:
                        c_list = self._interpolation(
                            e_list, c_list, method=self._interpolation_method
                        )(energies)
                        e_list = energies
                    return e_list, c_list

                case _:
                    # tidied up version of the previous function
                    data = np.loadtxt(
                        f"{self.db_path}{self.name}_{material}.txt",
                        skiprows=self.skip_rows,
                    )
                    e_list = self._nonuniquer(np.array(data[:, 0]))
                    c_list = np.array(data[:, self.col])
                    if energies is not None:
                        c_list = self._interpolation(
                            e_list, c_list, method=self._interpolation_method
                        )(energies)
                        e_list = energies

                    return e_list, c_list

    def _declare_new_columns(self, val: int) -> None:
        """Change the selected column using the deprecated API."""
        print(
            "Warning: _declare_new_columns is deprecated. Use change_column(new_col) instead."
        )
        self.change_column(val)

    def _generate_atomic_table(self) -> pd.DataFrame:
        """Build the atomic-number, weight, and density lookup table."""
        df = pd.read_csv(
            f"{DATABASE_DIR}/atomic_weight.db",
            delimiter="\t",
            header=0,
            usecols=[0, 1, 2, 3, 5],
            names=["Z", "Symbol", "Name", "Weight", "Density"],
            dtype={
                "Z": int,
                "Symbol": str,
                "Name": str,
                "Weight": str,
                "Density": float,
            },
        )
        df["Weight"] = df["Weight"].apply(self._parse_value)

        return df

    def _generate_material_list(self) -> list[str]:
        """Return material names available in the selected database."""
        self._fileslist = glob.glob(self.db_path + "*.txt")
        self._materials = set(Path(f).stem.split("_")[-1] for f in self._fileslist)
        return [f.split("_")[-1].split(".")[0] for f in self._fileslist]

    def _parse_value(self, val) -> float | str:
        """Parse an atomic weight value from the database format.

        Parameters
        ----------
        val : str
            Atomic weight value

        Returns
        -------
        float or str
            Parsed atomic weight value as a float, or the original string if parsing fails.
        """
        try:
            if "[" in val:
                return float(val[1:-1])
            else:
                f = val.split(".")
                # print(f)
                return float(".".join([f[0], f[1][0]]))
        except ValueError:
            return val

    def _nonuniquer(self, arr, offset=1e-7) -> np.ndarray:
        """Shifts the k-edge in material databases by 0.1 eV to enable interpolation at the edge.

        Parameters
        ----------
        arr : numpy.ndarray
            Energy values to adjust.
        offset : float, default=1e-7
            Increment applied.

        Returns
        -------
        numpy.ndarray
            Copy of ``arr`` with values shifted.
        """
        result = arr.copy()  # Create a copy of the input array to work with
        seen_values = {}  # A dictionary to store the count of each value

        for i in range(len(result)):
            if result[i] in seen_values:
                new_value = result[i] + offset
                while new_value in seen_values or new_value in result:
                    # Check for duplicates in both seen values and the new array
                    new_value += offset
                seen_values[new_value] = 1
                result[i] = new_value
            else:
                seen_values[result[i]] = 1
        assert np.all(np.diff(result) > 0), print(result)
        return result

    def _interpolation(self, e, sigma, method=pchip):
        """Interpolate cross-section data using the specified method.

        Parameters
        ----------
        e : numpy.ndarray
            Energy values.
        sigma : numpy.ndarray
            Cross-section values.
        method : callable, default=pchip
            Interpolation method to use. Must be a callable that takes two arguments (x, y) and returns an interpolating function.

        Returns
        -------
        callable
            Interpolating function that can be called with new energy values to obtain interpolated cross-section values.
        """
        return method(e, sigma)

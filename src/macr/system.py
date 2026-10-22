import numpy as np
import pandas as pd
from .material import Material
from .engine import Engine
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pickle
from typing import Self, Literal
import copy


class Layer:
    """Material with a thickness and active-detector flag.

    Attributes
    ----------
    material : Material
        The material of the layer.
    thickness : float
        The thickness of the layer in mm.
    active : bool
        Whether the layer contributes to the response matrix.
    """

    def __init__(self, material: Material, thickness: float, active: bool) -> None:
        """Initialise a layer.

        Parameters
        ----------
        material : Material
            Material represented by the layer.
        thickness : float
            Layer thickness in mm.
        active : bool
            Whether the layer is an active detector layer.
        """
        self.material = material
        self.thickness: float = thickness
        self.active: bool = active
        self.energies: np.ndarray = self.material.energies

    def get_transmission(self) -> np.ndarray:
        """Return transmission through this layer.

        Returns
        -------
        numpy.ndarray
            Transmission values for each energy.
        """
        return self.material.get_transmission(self.thickness)

    def get_absorption(self) -> np.ndarray:
        """Return absorption in this layer.

        Returns
        -------
        numpy.ndarray
            Absorption values for each energy.
        """
        return self.material.get_absorption(self.thickness)

    def set_energies(self, new_energies) -> None:
        """Regenerate cross-sections for new energies.

        Parameters
        ----------
        new_energies : array-like
            Energy values in MeV.
        """
        self.energies = new_energies
        self.regenerate_material()

    def set_engine(self, new_engine: Engine | str):
        """Replace the attenuation engine and recalculate cross-sections.

        Parameters
        ----------
        new_engine : Engine or str
            Engine instance or one of ``"NIST"``, ``"SRIM"``, ``"PSTAR"``,
            or ``"ESTAR"``.
        """
        if isinstance(new_engine, str):
            assert new_engine in ["NIST", "SRIM", "PSTAR", "ESTAR"]
            new_engine = Engine(new_engine)
        self.material.engine = new_engine
        self.regenerate_material()

    def regenerate_material(self):
        """Recalculate the material cross-sections at the layer energies."""
        self.material.update_cross_sections(self.energies)



class System:
    """Collection of layers used to calculate response matrices.

    Parameters
    ----------
    system : sequence of Layer or None, optional
        Initial layers. Layers can also be added with :meth:`add_layer`.
    """

    def __init__(self, system=None):
        # initialise system
        self.system = system

        # initialise attributes
        self.activeLayers = None
        self.activeCount = None
        self.initialEnergies = None
        self.numberLayers = 0
        # initialise response matrix
        self.rm = None

    def _initaliseEnergies(self):
        assert self.system != []
        if self.initialEnergies is None:
            self.initialEnergies = self.system[0].energies

    def _updateActive(self):
        """
        Generator function to grab active materials from list
        """
        self.activeLayers = [idx for idx, i in enumerate(self.system) if i.active]
        self.activeCount = len(self.activeLayers)
        self._updateCount()

    def _updateCount(self):
        self.numberLayers = len(self.system)

    # adding to system
    def add(self, additive: Literal[Layer, Self], idx: int = None):
        """Add a layer or another system.

        Parameters
        ----------
        additive : Layer or System
            Object to add.
        idx : int or None, optional
            Insertion index. Append when omitted.
        """
        if isinstance(additive, Layer):
            self.add_layer(additive, idx)
        elif isinstance(additive, System):
            self.add_system(additive, idx)
        else:
            pass

    def add_layer(self, layer: Layer, idx: int = None):
        """Add a layer to the system.

        Parameters
        ----------
        layer : Layer
            Layer to add.
        idx : int or None, optional
            Insertion index. Append when omitted.
        """
        if self.system is None:
            self.system = [layer]
        else:
            if idx is None:
                self.system.append(layer)
            else:
                self.system.insert(idx, layer)

        self._updateActive()

    def add_system(self, system: Self, idx: int = None):
        """Add each layer from another system in sequence."""
        for layer in system.system:
            self.add_layer(layer, idx)
        self._updateActive()

    # changing existing system
    def change_layer(self, layer: Layer, idx: int = -1):
        """Replace a layer by index.

        Parameters
        ----------
        layer : Layer
            Replacement layer.
        idx : int, default=-1
            Index of the layer to replace.
        """
        assert self.numberLayers > 0
        self.system[idx] = layer
        self._updateActive()

    def update_energies(self, new_energies):
        """Update all layers to use new energy values."""
        self.initialEnergies = new_energies

        for s in self:
            s.set_energies(new_energies)

    def update_engine(self, new_engine):
        """Update the attenuation engine for every layer."""
        for s in self:
            s.set_engine(new_engine)

        if self.rm is not None:
            self.generate_response()

    # processing system
    def generate_response(self, initial_intensity=None):
        """Generate the active-layer response matrix.

        Parameters
        ----------
        initial_intensity : array-like or None, optional
            Incident intensity at each energy. Uniform unit intensity is used
            when omitted.

        Notes
        -----
        The result is stored in :attr:`rm`.
        """
        self._initaliseEnergies()
        self._updateActive()

        self.rm = np.zeros((self.activeCount, len(self.initialEnergies)))

        if initial_intensity is None:
            ts = np.ones_like(self.initialEnergies)
        else:
            assert len(initial_intensity) == len(
                self.initialEnergies
            ), f"""Length of Initial_intensity {len(initial_intensity)} does 
                   not match length of material_energies {len(self.initialEnergies)}
                   If presupplinging initial intensity it must match energy array"""
            ts = initial_intensity

        count = 0
        for s in self.system:
            # compute layer transmisison
            t1 = s.get_transmission()
            if s.active:
                # compute layer absorption if active
                self.rm[count, :] = s.get_absorption() * ts * s.energies
                count += 1
            ts *= t1

    def get_profile(self, nstep=1000):
        """Calculate energy deposition throughout the layered system.

        Parameters
        ----------
        nstep : int, default=1000
            Number of depth steps.

        Notes
        -----
        Results are stored in :attr:`output` with energy, track, active-layer,
        and depth arrays.
        """
        # set target thickness as back of array
        cumulative_thickness = np.cumsum([s.thickness for s in self.system])
        thickness = cumulative_thickness[-1]
        dz = thickness / nstep

        # initialise arrays
        track_map = np.zeros((len(self.initialEnergies), nstep))
        energy_map = np.zeros((len(self.initialEnergies), nstep))
        active_steps = np.zeros((nstep,))
        layer_index = np.zeros((nstep,))

        # set initial energy
        energy_map[:, 0] = self.initialEnergies

        # initialise output
        self.output = {
            "energies": self.initialEnergies,
        }

        for n in range(1, nstep):
            current_zposition = n * dz
            loc = np.nonzero(current_zposition < cumulative_thickness)[0][0]

            # calculate track loss
            track = (
                self[loc].material.get_absorption(thickness / nstep)
                * energy_map[:, n - 1]
            )

            # calculate remaining energy
            delta_e = (
                self[loc].material.get_transmission(thickness / nstep)
                * energy_map[:, n - 1]
            )

            # update system
            self[loc].energies = np.clip(delta_e, 0, None)
            self[loc].regenerate_material()

            # update arrays
            energy_map[:, n] = self[loc].energies
            track_map[:, n] = track
            active_steps[n] = self[loc].active
            layer_index[n] = int(loc)

        # generate step positions for plotting
        zsteps = np.linspace(0, thickness, nstep)

        # reset material database:
        for s in self.system:
            s.energies = self.initialEnergies
            s.regenerate_material()

        self.output["energy_map"] = energy_map
        self.output["track_map"] = track_map
        self.output["active_steps"] = active_steps
        self.output["layer_index"] = layer_index
        self.output["zsteps"] = zsteps

        # return (track_map, energy_map, zsteps)

    def get_criticalenergies(self):
        """Calculate peak response energies and full-width edges."""
        if "energy_map" not in self.output.keys():
            self.get_profile()

        critical_energies = np.zeros(len(self))
        critical_edges = np.zeros((2, len(self)))

        for index, n in enumerate(np.unique(self.output["layer_index"])):
            boolMap = self.output["layer_index"] == n
            maskedTrack = self.output["track_map"] * boolMap
            layerResponse = np.sum(maskedTrack, axis=1)

            ## determine FWHM and Peak Location
            peaks, properties = find_peaks(
                layerResponse, np.max(layerResponse), width=1
            )
            # print(f'the found peaks are: {peaks}')
            critical_energies[index] = np.squeeze(self.initialEnergies[peaks])
            critical_edges[0, index] = np.array(
                [self.initialEnergies[int(p)] for p in [properties["left_ips"]]]
            )
            critical_edges[1, index] = np.array(
                [self.initialEnergies[int(p)] for p in [properties["right_ips"]]]
            )

        self.output["critical_energy"] = critical_energies
        self.output["critical_edges"] = critical_edges

    #### Presenting the array
    def plot_schematic(self, ax=None, yoff=0, seperator=True, colors=None):
        """Plot the layered system geometry.

        Parameters
        ----------
        ax : matplotlib.axes.Axes or None, optional
            Axes on which to draw. A new axes is created when omitted.
        yoff : float, default=0
            Vertical offset for the schematic.
        seperator : bool, default=True
            Whether to draw the baseline separator.
        colors : sequence or None, optional
            Colors used for distinct materials.
        """
        # assign colors
        prop_cycle = plt.rcParams["axes.prop_cycle"]
        if colors is None:
            colors = prop_cycle.by_key()["color"]

        # generate unique materials for legend
        material_order = []
        length_order = []
        for key in self.system:
            material_order.append(key.material.materialstr)
            length_order.append(key.thickness)

        legendentry = []
        obs = {}
        for idx, o in enumerate(np.unique(material_order)):
            obs[o] = colors[idx]
            legendentry.append(Patch(facecolor=colors[idx], alpha=0.25))

        # plot patches
        x = 0
        if ax is None:
            fig, ax = plt.subplots(1, 1)

        for length, mat in zip(length_order, material_order):
            x2 = x + length

            ax.fill_between(
                [x, x2],
                [yoff, yoff],
                [1 + yoff, 1 + yoff],
                facecolor=obs[mat],
                edgecolor="k",
                alpha=0.25,
            )

            # reset x for next time
            x = np.copy(x2)

        if seperator:
            ax.plot([0, x2], [yoff, yoff], "k-")
        ax.set_xlabel("z (mm)")
        ax.legend(legendentry, obs, loc="center left", bbox_to_anchor=(1, 0.5))

    def plot_response(self, ax=None, ylim=[1e-4, None]):
        """Plot the generated response matrix.

        Parameters
        ----------
        ax : matplotlib.axes.Axes or None, optional
            Axes on which to draw.
        ylim : sequence, default=[1e-4, None]
            Y-axis limits.
        """
        if ax is None:
            fig, ax = plt.subplots(1, 1)

        for i, r in enumerate(self.rm):
            ax.plot(self.initialEnergies, r)

        ax.plot(self.initialEnergies, self.initialEnergies, "k--")

        ax.set_ylim(ylim)
        ax.set_yscale("log")
        ax.set_xscale("log")
        ax.set_xlabel("Energy (MeV)")
        ax.set_ylabel("Absorbed Energy (MeV)")

    ### deal with dumping and loading the system back
    def to_dataframe(self):
        """Return layer properties as a pandas DataFrame."""
        out = {
            "Name": [s.material.materialstr for s in self],
            "Compound": [s.material.material for s in self],
            "Thickness": [s.thickness for s in self],
            "Density": [s.material.density for s in self],
            "Active Flag": [s.active for s in self],
        }

        return pd.DataFrame.from_dict(out, orient="index").T

    def _saveSystem(self, file):
        with open(file, "wb") as f:
            pickle.dump(self.__dict__, f)

    def _loadSystem(self, file):
        with open(file, "rb") as f:
            self.__dict__ = pickle.load(f)

    ## generics
    def __getitem__(self, index: int) -> Layer:
        """Return the layer at ``index``."""
        return self.system[index]

    def __len__(self):
        return len(self.system)

    # depreciating metods
    def addLayer(self, layer: Layer, idx: int = None):
        """Deprecated alias for :meth:`add_layer`."""
        self.add_layer(layer, idx)

    def changeLayer(self, layer: Layer, idx=-1):
        """Deprecated alias for :meth:`change_layer`."""
        self.change_layer(layer, idx)

    def addSystem(self, system: Self):
        """Deprecated alias for :meth:`add_system`."""
        self.add_system(system)

    def updateEnergies(self, new_energies):
        """Deprecated alias for :meth:`update_energies`."""
        self.update_energies(new_energies)

    def updateEngine(self, new_engine):
        """Deprecated alias for :meth:`update_engine`."""
        self.update_engine(new_engine)

    def generateResponse(self, initial_intensity=None):
        """Deprecated alias for :meth:`generate_response`."""
        self.generate_response(initial_intensity)


class LinearBuilder(System):
    """System variant exposing one response row per indexed layer."""

    def __init__(self, system=None):
        System.__init__(self, system)
        self.type = "Linear"

    def __getitem__(self, index: int) -> np.ndarray:
        """Return a response-matrix row for an active layer."""
        if self.rm is None:
            self.generate_response()
        return self.rm[self.activeLayers[index], :]


class ArealBuilder(System):
    """Build a response matrix for a global system and areal filters.

    Parameters
    ----------
    global_system : System
        Common filter and detector layers.
    filter_system : sequence of System or Layer
        Passive filter regions. Active layers are ignored.

    The resulting response matrix contains one block per filter region. It is
    good practice to exclude active layers from ``filter_system``.
    """

    def __init__(
        self, global_system: System = None, filter_system: list[System | Layer] = None
    ):
        """Initialize an areal response-matrix builder.

        Parameters
        ----------
        global_system : System or None, optional
            Common filter and detector layers.
        filter_system : list of System or Layer or None, optional
            Filter regions to apply to the global system.
        """
        System.__init__(self, global_system)
        self.type = "Areal"

        self.global_system = global_system
        self.filter_system = filter_system

    def _build_rm(self):

        # clean system
        self._initaliseEnergies()
        self._updateActive()

        # calculate necessary size
        self.rm = np.zeros(
            (
                len(self.filter_system),
                len(self.global_system.activeLayers),
                len(self.initialEnergies),
            )
        )

        for idx, local_filter in enumerate(self.filter_system):
            rm = copy.deepcopy(self.global_system)
            # adds entry at beginning of array - potentially allow more explicit positions later?
            rm.add(local_filter, 0)
            # update and generate response for subsystem
            rm.updateEnergies(self.initialEnergies)
            rm.generate_response()

            # apply to super system
            for jdx in range(len(self.global_system.activeLayers)):
                self.rm[idx, jdx, :] = rm.rm[jdx, :]

        # enforce reduced dimensions where possible
        if len(self.global_system.activeLayers) == 1:
            """ 
            Needs to happen at end to ensure address is correct for build
            """
            self.rm = np.squeeze(self.rm)

    def generate_response(self, initial_intensity=None):
        """Generate the areal response matrix.

        Parameters
        ----------
        initial_intensity : array-like or None, optional
            Incident intensity at each energy. Uniform unit intensity is used
            when omitted.
        """
        self._build_rm()
        if initial_intensity is None:
            ts = np.ones_like(self.initialEnergies)
        else:
            assert len(initial_intensity) == len(
                self.initialEnergies
            ), f"""Length of Initial_intensity {len(initial_intensity)} does 
                   not match length of material_energies {len(self.initialEnergies)}
                   If presupplinging initial intensity it must match energy array"""
            ts = initial_intensity

        self.rm *= ts

    def __getitem__(self, index: int) -> np.ndarray:
        """Return a response-matrix row for an active layer."""
        if self.rm is None:
            self.generate_response()
        return self.rm[self.activeLayers[index], :]

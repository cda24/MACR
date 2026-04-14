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
    """
    Declarations of material with specific thickness and active flag for use in System
    Attributes
    ----------
    material : Material class
        The material of the layer.
    thickness : float
        The thickness of the layer in mm.
    active : boolean
        flag to indicate if layer is active or not.
    """

    def __init__(self, material: Material, thickness: float, active: bool):
        """
        Initialises a Layer with a Material and thickness.

        The material of the layer - type, Material
        The thickness of the layer in mm - type, Float
        Flag to indicate active or not - type, Bool
        """
        self.material = material
        self.thickness: float = thickness
        self.active: bool = active
        self.energies: np.ndarray = self.material.energies

    def _add_area(self, x, y, z):
        """
        Placeholder function for eventual areal version of the script
        Currently does nothing.
        """
        self.x = x
        self.y = y
        self.z = z

    def get_transmission(self):
        """
        Exposes the Material get_transmission function
        """
        return self.material.get_transmission(self.thickness)

    def get_absorption(self):
        """
        Exposes the Material get_transmission function
        """
        return self.material.get_absorption(self.thickness)

    def set_energies(self, new_energies):
        """
        Regenerate cross-sections for new energies
        """
        self.energies = new_energies
        self.regenerate_material()

    def set_engine(self, new_engine: Engine | str):
        if isinstance(new_engine, str):
            assert new_engine in ["NIST", "SRIM", "PSTAR", "ESTAR"]
            new_engine = Engine(new_engine)
        self.material.engine = new_engine
        self.regenerate_material()

    def regenerate_material(self):
        self.material.update_cross_sections(self.energies)


class System:
    """
    List of Materials and thickness to streamline building of response matrices

    Input should be defined as a series of Layers either in one go:
        [Layer, Layer,...]
    Or via sequential add_layer commands:
        system = System()
        system.add_layer(Layer)
        system.add_layer(Layer)
        system.add_system(System)

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

        if self.system is not None:
            self.generate_response()

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
        if isinstance(additive, Layer):
            self.add_layer(additive, idx)
        elif isinstance(additive, System):
            self.add_system(additive, idx)
        else:
            pass

    def add_layer(self, layer: Layer, idx: int = None):
        """
        Forces reset on initalisation
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
        for layer in system.system:
            self.add_layer(layer, idx)
        self._updateActive()

    # changing existing system
    def change_layer(self, layer: Layer, idx: int = -1):
        """
        Changes layer by index in the system
        By default index is set to last layer.
        """
        assert self.numberLayers > 0
        self.system[idx] = layer
        self._updateActive()

    def update_energies(self, new_energies):
        self.initialEnergies = new_energies

        for s in self:
            s.set_energies(new_energies)

    def update_engine(self, new_engine):
        for s in self:
            s.set_engine(new_engine)

        if self.rm is not None:
            self.generate_response()

    # processing system
    def generate_response(self, initial_intensity=None):
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
        """
        Returns the z profile deposition for radiation transmitting through
        Thickness in mm, nstep is number of elements calculated
        By default this is 1000 so the resolution is thickness/nstep.

        Solved for the full array, particles are tracked until they run out of energy

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
        """
        Plots dictionary generated by buildRail in a readable format.
        Includes lengths and colours for distinct materials
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
        """
        Pretty_print function for the system
        Mainly for debugging and checking.
        """
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
        """
        Returns the layer at the index.

        :param index: The index of the layer.
        :type index: int
        """
        return self.system[index]

    def __len__(self):
        return len(self.system)

    # depreciating metods
    def addLayer(self, layer: Layer, idx: int = None):
        """
        `Depreciating` use `add_layer` instead
        Forces reset on initalisation
        """
        self.add_layer(layer, idx)

    def changeLayer(self, layer: Layer, idx=-1):
        """
        `Depreciating` use `change_layer` instead
        Changes layer by index in the system
        By default index is set to last layer.
        """
        self.change_layer(layer, idx)

    def addSystem(self, system: Self):
        """
        `Depreciating` use `add_system` instead
        Adds system to current system, layers are added sequentially
        """
        self.add_system(system)

    def updateEnergies(self, new_energies):
        """
        `Depreciating` use `update_energies` instead
        Regenerate cross-sections for new energies
        """
        self.update_energies(new_energies)

    def updateEngine(self, new_engine):
        """
        `Depreciating` use `update_engine` instead
        Regenerate cross-sections for new engine
        """
        self.update_engine(new_engine)

    def generateResponse(self, initial_intensity=None):
        """
        `Depreciating` use `generate_response` instead
         Generates response matrix for system, if initial_intensity is provided it will be used as the initial intensity of the system, otherwise it will be assumed to be 1 for all energies.
        """
        self.generate_response(initial_intensity)


class LinearBuilder(System):
    def __init__(self, system=None):
        System.__init__(self, system)
        self.type = "Linear"

    def __getitem__(self, index: int) -> np.ndarray:
        """
        Overrides the system __getitem__ method to retrieve entry in the response matrix
        """
        if self.rm is None:
            self.generate_response()
        return self.rm[self.activeLayers[index], :]


class ArealBuilder(System):
    """
    Builds a flat response matrix for a global filter/detector set and individual filters

    `Global_system` should be a macr.System that are common to all aspects of the areal filters
    `Filter_system` is a list of macr.System or macr.Layer corresponding to unique regions in the filter pack these are exclusively passive layers, active layers supplied in the filter_system are ignored

    The response matrix is built as an array with size:
        [Energies, len(filter_system) * global_system.activeLayers]

    For a global_system with a single active layer:
        self.rm[0,:] -> filter_system[0]
        self.rm[N,:] -> filter_system[N]

    For a global_system with M active layers:
        self.rm[0,0,:] -> filter_system[0], global_system[global_system.activeLayers[0]]
        self.rm[N,M,:] -> filter_system[N], global_system[global_system.activeLayers[M]]

    Good practice should exclude active layers from the filter_system but this is not strictly prohibited
    """

    def __init__(
        self, global_system: System = None, filter_system: list[System | Layer] = None
    ):
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
        """
        Overrides the System generate to avoid clashes
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
        """
        Overrides the system __getitem__ method to retrieve entry in the response matrix
        """
        if self.rm is None:
            self.generate_response()
        return self.rm[self.activeLayers[index], :]

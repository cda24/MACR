import numpy as np
import pandas as pd
from .material import Material
from .engine import Engine
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pickle
from typing import Self


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

    def __init__(self, system=None, system_id: str = None):
        # initialise system
        self.system = system
        self.system_id = system_id

        # initialise attributes
        self.activeLayers = None
        self.activeCount = None
        self.initialEnergies = None
        self.numberLayers = 0
        # initialise response matrix
        self.rm = None

    # hidden methods
    def _initaliseEnergies(self):
        assert self.system != []
        if self.initialEnergies is None:
            self.initialEnergies = self[0].energies

    def _updateActive(self):
        """
        Generator function to grab active materials from list
        """
        self.activeLayers = [idx for idx, i in enumerate(self.system) if i.active]
        self.activeCount = len(self.activeLayers)
        self._updateCount()

    def _updateCount(self):
        self.numberLayers = len(self.system)

    def add_layer(self, layer: Layer):
        """
        Forces reset on initalisation
        """
        if self.system is None:
            self.system = [layer]
        else:
            self.system.append(layer)

        self._updateActive()

    def change_layer(self, layer: Layer, idx=-1):
        """
        Changes layer by index in the system
        By default index is set to last layer.
        """
        assert self.numberLayers > 0
        self.system[idx] = layer
        self._updateActive()

    def add_system(self, system: Self):
        for layer in system.system:
            self.add_layer(layer)
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

        df = pd.DataFrame.from_dict(out, orient="index").T

        # Add system ID to output
        if self.system_id:
            df.insert(0, "System ID", self.system_id)

        return df

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
    def addLayer(self, layer: Layer):
        """
        `Depreciating` use `add_layer` instead
        Forces reset on initalisation
        """
        self.add_layer(layer)

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


class _System:
    """
    Array of Material instances in a series
    Dedicated class to handle RCF and LAS style distributions

    Input can be defined as System array:
        [nist.Material, thickness, active_flag]

    Or by a series of System.add_layer() commands

    Main additional functions is the rewrite of get_profile
    to handle cross-material trajectories
    """

    def __init__(self, system_dict=None, verbose=False):
        assert type(verbose) is bool

        ## Sanitise system import
        assert (type(system_dict) is type(None)) or (type(system_dict) == dict)
        self.initialEnergies = None

        self.verbose = verbose
        if type(system_dict) is type(None):
            if self.verbose:
                print("System is empty, use System.add_layer()")
            self.system = {}
            self.count = 0
        else:
            if self.verbose:
                print("System loaded")
            self.system = system_dict
            self.count = len(self.system.keys())
            self._initEnergies()

        ## Assertion check for each layer
        if self.count:
            self._check_system()

    def _updateComponents(self):
        self.active_layers = np.squeeze(
            np.argwhere([s[2] for s in self.system.values()])
        )

    def _check_system(self):
        for i, s in enumerate(self.system.values()):
            assert isinstance(s[0], Material), (
                f"Layer {i} is not type(Material) it is {type(s[0])}"
            )
        self._updateComponents()

    def _initEnergies(self):
        if self.initialEnergies is None:
            idx = list(self.system.keys())[0]
            self.initialEnergies = self.system[idx][0].energies

    def add_layer(self, material, thickness, active=1, index=None):
        if index is None:
            index = self.count
        self.system[f"A{index}"] = [material, thickness, active]
        self.count = len(self.system.keys())

        if self.verbose:
            print(f"Added {material, thickness, active} to index {index}")
        self._initEnergies()
        self._updateComponents()

    def add_system(self, system, index=None):
        assert isinstance(system, System)
        if index is None:
            index = self.count

        for s in system.system.keys():
            self.add_layer(*system.system[s])
        self._initEnergies()
        self._updateComponents()

    def get_profile(self, nstep=1000):
        """
        Returns the z profile deposition for radiation transmitting through
        Thickness in mm, nstep is number of elements calculated
        By default this is 1000 so the resolution is thickness/nstep.

        Solved for the full array, particles are tracked until they run out of energy

        """
        # set target thickness as back of array
        cumulative_thickness = np.cumsum([s[1] for s in self.system.values()])
        thickness = cumulative_thickness[-1]
        dz = thickness / nstep

        # initialise seed energies
        hold_energies = self.system[f"A0"][0].energies

        # initialise arrays
        track_map = np.zeros((len(self.system[f"A0"][0].energies), nstep))
        energy_map = np.zeros((len(self.system[f"A0"][0].energies), nstep))
        active_steps = np.zeros((nstep,))
        layer_index = np.zeros((nstep,))

        # set initial energy
        energy_map[:, 0] = self.system[f"A0"][0].energies

        # initialise output
        self.output = {
            "energies": self.system[f"A0"][0].energies,
        }

        for n in range(1, nstep):
            current_zposition = n * dz
            loc = np.nonzero(current_zposition < cumulative_thickness)[0][0]

            # calculate track loss
            track = (
                self.system[f"A{loc}"][0].get_absorption(thickness / nstep)
                * energy_map[:, n - 1]
            )

            # calculate remaining energy
            delta_e = (
                self.system[f"A{loc}"][0].get_transmission(thickness / nstep)
                * energy_map[:, n - 1]
            )

            # update system
            self.system[f"A{loc}"][0].energies = np.clip(delta_e, 0, None)
            self.system[f"A{loc}"][0].update_cross_sections(
                self.system[f"A{loc}"][0].energies
            )

            # update arrays
            energy_map[:, n] = self.system[f"A{loc}"][0].energies
            track_map[:, n] = track
            active_steps[n] = self.system[f"A{loc}"][2]
            layer_index[n] = int(loc)

        # generate step positions for plotting
        zsteps = np.linspace(0, thickness, nstep)

        # reset material database:
        for s in self.system.values():
            s[0].energies = self.initialEnergies
            s[0].update_cross_sections(self.initialEnergies)

        self.output["energy_map"] = energy_map
        self.output["track_map"] = track_map
        self.output["active_steps"] = active_steps
        self.output["layer_index"] = layer_index
        self.output["zsteps"] = zsteps

        # return (track_map, energy_map, zsteps)

    def get_criticalenergies(self):
        try:
            if "energy_map" not in self.output.keys():
                self.get_profile()
        except:
            self.get_profile()

        critical_energies = np.zeros(len(self.system.values()))
        critical_edges = np.zeros((2, len(self.system.values())))

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
    def plot_array_dict(self, ax=None, yoff=0, seperator=True, colors=None):
        """
        Plots dictionary generated by buildRail in a readable format.
        Includes lengths and colours for distinct materials
        """
        # assign colors
        prop_cycle = plt.rcParams["axes.prop_cycle"]

        if colors is None:
            colors = prop_cycle.by_key()["color"]

        material_order = []

        for key in self.system:
            s = self.system[key]
            material_order.append(s[0].materialstr)

        obs = {}
        legendentry = []
        for idx, o in enumerate(np.unique(material_order)):
            obs[o] = colors[idx]
            legendentry.append(Patch(facecolor=colors[idx], alpha=0.25))

        x = 0
        if ax is None:
            fig, ax = plt.subplots(1, 1)

        material_order = []
        length_order = []
        for s in self.system:
            key = self.system[s]
            material_order.append(key[0].materialstr)
            length_order.append(key[1])

        for idx, mat in enumerate(material_order):
            y = 0 + yoff
            y2 = 1 + yoff
            x2 = x + length_order[idx]
            # ax.add_patch(rect)

            xs = [x, x2]
            ys1 = [y, y]
            ys2 = [y2, y2]

            ax.fill_between(xs, ys1, ys2, facecolor=obs[mat], alpha=0.25)
            # ax.plot([x2, x2], [y, y2], 'k--', lw=1)
            x = np.copy(x2)

        if seperator:
            ax.plot([0, x2], [y, y], "k-")
        ax.set_xlabel("z (mm)")
        ax.legend(legendentry, obs, loc="center left", bbox_to_anchor=(1, 0.5))

    def to_dataframe(self):
        """
        Pretty_print function for the system
        Mainly for debugging and checking.
        """
        df = pd.DataFrame.from_dict(
            self.system,
            orient="index",
            columns=["Material Obj", "Thickness", "Active Flag"],
        )
        df["Name"] = [self.system[key][0].materialstr for key in self.system.keys()]
        df["Density"] = [self.system[key][0].density for key in self.system.keys()]
        df["Compound"] = [self.system[key][0].material for key in self.system.keys()]
        return df.reindex(
            columns=[
                "Name",
                "Material Obj",
                "Thickness",
                "Density",
                "Compound",
                "Active Flag",
            ]
        )

    ### deal with dumping and loading the system back
    def _dumpSystem(self, file):
        with open(file, "wb") as f:
            data = self.system
            print(type(data))
            pickle.dump(data, f)

    def _loadSystem(self, file):
        with open(file, "rb") as f:
            print(pickle.load(f))

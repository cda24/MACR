Quickstart
==========

Creating a material
-------------------

Create a :class:`macr.material.Material` by providing a chemical formula, density in g/cc, and optionally an energy array in MeV. If no energies are provided, the default values for the selected engine are used.

.. code-block:: python

   import numpy as np
   from macr.material import Material

   energies = np.linspace(0.01, 1.0, 100)
   aluminium = Material(
       material="Al",
       density=2.71,
       energies=energies,
       engine="NIST",
   )

   transmission = aluminium.get_transmission(thickness=1.0)
   absorption = aluminium.get_absorption(thickness=1.0)

``thickness`` is measured in millimetres. The returned arrays have one value
for each input energy.

Building a layered system
-------------------------

Use :class:`macr.system.Layer` to give a material a thickness and identify
whether it is an active detector layer. Add layers to a
:class:`macr.system.System` and generate its response matrix:

.. code-block:: python

   from macr.material import Material
   from macr.system import Layer, System

   filter_material = Material("Al", density=2.71)
   detector_material = Material("CsI", density=4.51)

   system = System()
   system.add_layer(Layer(filter_material, thickness=0.1, active=False))
   system.add_layer(Layer(detector_material, thickness=0.1, active=True))
   system.generate_response()

The response matrix is available as ``system.rm``. 
Its rows correspond to active layers and its columns correspond to the system's initial energies.
Use ``system.plot_response()`` to display the response or ``system.to_dataframe()`` to inspect the layer configuration.

Choosing an engine
------------------

The supported engine names are ``"NIST"``, ``"ESTAR"``, ``"PSTAR"``, and ``"SRIM"``. 
Select an engine when constructing a material, or create and reuse an :class:`macr.engine.Engine` instance when constructing many materials.

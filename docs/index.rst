MACR documentation
==================

**MACR** (pronounced *maker*) - The Material Attenuation Calculator for Radiation - is a python library to generate interaction cross-sections of any material for protons (NIST PSTAR and SRIM), electrons (NIST ESTAR), and x-rays (NIST XCOM).

It contains a database of cross-sections for each element, which are then combined according to their atomic weight to provide cross-sections for materials and compounds. 
The library can be used to calculate the transmission and absorption through multiple layers of different materials.
The library includes cross-section data for the NIST XCOM, ESTAR, PSTAR, and SRIM engines.

The setup instructions are available in the :doc:`installation` guide.
Start with the :doc:`quickstart` guide, or browse the :doc:`api` reference for the available classes and methods.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

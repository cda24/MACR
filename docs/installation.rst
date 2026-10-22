Installation
============

Install MACR from a local checkout while developing:

.. code-block:: console

   git clone https://github.com/cda24/MACR.git
   cd MACR
   python -m pip install -e .

The project requires Python 3.11 or newer. 

Developer
-----------
The optional ``test`` dependency includes ``pytest`` for running the unit tests.

.. code-block:: console

   python -m pip install -e '.[test]'

Building the documentation
--------------------------
The optional ``docs`` dependency includes Sphinx and the type-hint extension used to build this documentation.

.. code-block:: console

   python -m pip install -e '.[docs]'


From the repository root, run:

.. code-block:: console

   sphinx-build -b html docs docs/_build/html

The generated site is available at ``docs/_build/html/index.html``.

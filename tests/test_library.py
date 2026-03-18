import pytest
import  macr.library as library
import macr.library.scintillators as scintillators
import macr.library.ip as ip
import macr.library.rcf as rcf
import macr.library.elements as elements

@pytest.fixture
def scintillator_names():
    return ['ANTHRACENE', 'BGO', 'CH', 'CsI', 'GADOX', 'LANEX', 'LSO', 'LYSO', 'LuAG', 'YAG']

@pytest.fixture
def rcf_names():
    return ['EBT_V3', 'EBT_XD', 'HD_V2', 'XR_RV3']

@pytest.fixture
def ip_names():
    return ['IP_MS', 'IP_SR', 'IP_TR']

@pytest.fixture
def element_names():
    return ['Ac', 'Ag', 'Al', 'Am', 'Ar', 'As', 'At', 'Au', 'B', 'Ba', 'Be', 'Bi', 'Bk', 'Br', 'C', 'Ca', 'Cd', 'Ce', 'Cf', 'Cl', 'Cm', 'Co', 'Cr', 'Cs', 'Cu', 'Dy', 'Er', 'Eu', 'F', 'Fe', 'Fr', 'Ga', 'Gd', 'Ge', 'H', 'He', 'Hf', 'Hg', 'Ho', 'I', 'In', 'Ir', 'K', 'Kr', 'La', 'Li', 'Lu', 'Mg', 'Mn', 'Mo', 'N', 'Na', 'Nb', 'Nd', 'Ne', 'Ni', 'Np', 'O', 'Os', 'P', 'Pa', 'Pb', 'Pd', 'Pm', 'Po', 'Pr', 'Pt', 'Pu', 'Ra', 'Rb', 'Re', 'Rh', 'Rn', 'Ru', 'S', 'Sb', 'Sc', 'Se', 'Si', 'Sm', 'Sn', 'Sr', 'Ta', 'Tb', 'Tc', 'Te', 'Th', 'Ti', 'Tl', 'Tm', 'U', 'V', 'W', 'Xe', 'Y', 'Yb', 'Zn', 'Zr']

def test_scintillator_names(scintillator_names):
    for name in scintillator_names:
        assert name in dir(scintillators)

def test_rcf_names(rcf_names):
    for name in rcf_names:
        assert name in dir(rcf)

def test_ip_names(ip_names):
    for name in ip_names:
        assert name in dir(ip)

def test_element_names(element_names):
    for name in element_names:
        assert name in dir(elements)

def test_all_materials_imported(scintillator_names, rcf_names, ip_names, element_names):
    for name in scintillator_names+rcf_names+ip_names+element_names:
        assert name in dir(library)

def test_all_materials_have_nist_engine():
    for name in dir(library):
        obj = getattr(library, name)
        if isinstance(obj, library.Material):
            assert obj.engine.name == "NIST", f"Material {name} does not have NIST engine, has {obj.engine.name}"
"""Predefined materials from the Geant4 NIST material database.

Each exported symbol is a :class:`macr.material.Material` configured with the
corresponding compound composition and density.
"""

from ..material import Material
from ..library import ENERGIES, ENGINE

# region - G4Nist Materials
ACETONE = Material("C3H6O", 0.7899, generic_name="ACETONE", energies=ENERGIES, engine=ENGINE)
ACETYLENE = Material("C2H2", 0.0010967, generic_name="ACETYLENE", energies=ENERGIES, engine=ENGINE)
ADENINE = Material("C5H5N5", 1.6, generic_name="ADENINE", energies=ENERGIES, engine=ENGINE)
ADIPOSE_TISSUE_ICRP = Material(
    "H0.114C0.598N0.007O0.278Na0.001S0.001Cl0.001",
    0.95,
    generic_name="ADIPOSE_TISSUE_ICRP",
    energies=ENERGIES,
    engine=ENGINE
)
AIR = Material(
    "C0.000124N0.755268O0.231781Ar0.012827",
    0.00120479,
    generic_name="AIR",
    energies=ENERGIES,
    engine=ENGINE
)
ALANINE = Material("C3H7NO2", 1.42, generic_name="ALANINE", energies=ENERGIES, engine=ENGINE)
ALUMINUM_OXIDE = Material(
    "Al2O3", 3.97, generic_name="ALUMINUM_OXIDE", energies=ENERGIES, engine=ENGINE
)
AMBER = Material(
    "H0.10593C0.788974O0.105096", 1.1, generic_name="AMBER", energies=ENERGIES, engine=ENGINE
)
AMMONIA = Material("NH3", 0.000826019, generic_name="AMMONIA", energies=ENERGIES, engine=ENGINE)
ANILINE = Material("C6H7N", 1.0235, generic_name="ANILINE", energies=ENERGIES, engine=ENGINE)
ANTHRACENE = Material("C14H10", 1.283, generic_name="ANTHRACENE", energies=ENERGIES, engine=ENGINE)
BAKELITE = Material(
    "H0.057441C0.774591O0.167968", 1.25, generic_name="BAKELITE", energies=ENERGIES, engine=ENGINE
)
BARIUM_FLUORIDE = Material(
    "BaF2", 4.89, generic_name="BARIUM_FLUORIDE", energies=ENERGIES, engine=ENGINE
)
BARIUM_SULFATE = Material("BaSO4", 4.5, generic_name="BARIUM_SULFATE", energies=ENERGIES, engine=ENGINE)
BENZENE = Material("C6H6", 0.87865, generic_name="BENZENE", energies=ENERGIES, engine=ENGINE)
BERYLLIUM_OXIDE = Material(
    "BeO", 3.01, generic_name="BERYLLIUM_OXIDE", energies=ENERGIES, engine=ENGINE
)
BGO = Material("Bi4Ge3O12", 7.13, generic_name="BGO", energies=ENERGIES, engine=ENGINE)
BLOOD_ICRP = Material(
    "H0.102C0.11N0.033O0.745Na0.001P0.001S0.002Cl0.003K0.002Fe0.001",
    1.06,
    generic_name="BLOOD_ICRP",
    energies=ENERGIES,
    engine=ENGINE
)
BONE_COMPACT_ICRU = Material(
    "H0.064C0.278N0.027O0.41Mg0.002P0.07S0.002Ca0.147",
    1.85,
    generic_name="BONE_COMPACT_ICRU",
    energies=ENERGIES,
    engine=ENGINE
)
BONE_CORTICAL_ICRP = Material(
    "H0.034C0.155N0.042O0.435Na0.001Mg0.002P0.103S0.003Ca0.225",
    1.92,
    generic_name="BONE_CORTICAL_ICRP",
    energies=ENERGIES,
    engine=ENGINE
)
BORON_CARBIDE = Material("B4C", 2.52, generic_name="BORON_CARBIDE", energies=ENERGIES, engine=ENGINE)
BORON_OXIDE = Material("B2O3", 1.812, generic_name="BORON_OXIDE", energies=ENERGIES, engine=ENGINE)
BRAIN_ICRP = Material(
    "H0.107C0.145N0.022O0.712Na0.002P0.004S0.002Cl0.003K0.003",
    1.04,
    generic_name="BRAIN_ICRP",
    energies=ENERGIES,
    engine=ENGINE
)
BUTANE = Material("C4H10", 0.00249343, generic_name="BUTANE", energies=ENERGIES, engine=ENGINE)
CADMIUM_TELLURIDE = Material(
    "CdTe", 6.2, generic_name="CADMIUM_TELLURIDE", energies=ENERGIES, engine=ENGINE
)
CADMIUM_TUNGSTATE = Material(
    "CdWO4", 7.9, generic_name="CADMIUM_TUNGSTATE", energies=ENERGIES, engine=ENGINE
)
CALCIUM_CARBONATE = Material(
    "CaCO3", 2.8, generic_name="CALCIUM_CARBONATE", energies=ENERGIES, engine=ENGINE
)
CALCIUM_FLUORIDE = Material(
    "CaF2", 3.18, generic_name="CALCIUM_FLUORIDE", energies=ENERGIES, engine=ENGINE
)
CALCIUM_OXIDE = Material("CaO", 3.3, generic_name="CALCIUM_OXIDE", energies=ENERGIES, engine=ENGINE)
CALCIUM_SULFATE = Material(
    "CaSO4", 2.96, generic_name="CALCIUM_SULFATE", energies=ENERGIES, engine=ENGINE
)
CALCIUM_TUNGSTATE = Material(
    "CaWO4", 6.062, generic_name="CALCIUM_TUNGSTATE", energies=ENERGIES, engine=ENGINE
)
CARBON_DIOXIDE = Material(
    "CO2", 0.00184212, generic_name="CARBON_DIOXIDE", energies=ENERGIES, engine=ENGINE
)
CARBON_TETRACHLORIDE = Material(
    "CCl4", 1.594, generic_name="CARBON_TETRACHLORIDE", energies=ENERGIES, engine=ENGINE
)
CELLULOSE_CELLOPHANE = Material(
    "C6H10O5", 1.42, generic_name="CELLULOSE_CELLOPHANE", energies=ENERGIES, engine=ENGINE
)
CELLULOSE_BUTYRATE = Material(
    "H0.067125C0.545403O0.387472",
    1.2,
    generic_name="CELLULOSE_BUTYRATE",
    energies=ENERGIES,
    engine=ENGINE
)
CELLULOSE_NITRATE = Material(
    "H0.029216C0.271296N0.121276O0.578212",
    1.49,
    generic_name="CELLULOSE_NITRATE",
    energies=ENERGIES,
    engine=ENGINE
)
CERIC_SULFATE = Material(
    "H0.107596N0.0008O0.874976S0.014627Ce0.002001",
    1.03,
    generic_name="CERIC_SULFATE",
    energies=ENERGIES,
    engine=ENGINE
)
CESIUM_FLUORIDE = Material(
    "CsF", 4.115, generic_name="CESIUM_FLUORIDE", energies=ENERGIES, engine=ENGINE
)
CESIUM_IODIDE = Material("CsI", 4.51, generic_name="CESIUM_IODIDE", energies=ENERGIES, engine=ENGINE
)
CHLOROBENZENE = Material(
    "C6H5Cl", 1.1058, generic_name="CHLOROBENZENE", energies=ENERGIES, engine=ENGINE
)
CHLOROFORM = Material("CHCl3", 1.4832, generic_name="CHLOROFORM", energies=ENERGIES, engine=ENGINE
)
CONCRETE = Material(
    "H0.01C0.001O0.529107Na0.016Mg0.002Al0.033872Si0.337021K0.013Ca0.044Fe0.014",
    2.3,
    generic_name="CONCRETE",
    energies=ENERGIES,
    engine=ENGINE
)
CYCLOHEXANE = Material("C6H12", 0.779, generic_name="CYCLOHEXANE", energies=ENERGIES, engine=ENGINE)
DICHLORODIETHYL_ETHER = Material(
    "C4H8OCl2", 1.2199, generic_name="DICHLORODIETHYL_ETHER", energies=ENERGIES, engine=ENGINE
)
DIETHYL_ETHER = Material(
    "C4H10O", 0.71378, generic_name="DIETHYL_ETHER", energies=ENERGIES, engine=ENGINE
)
DIMETHYL_SULFOXIDE = Material(
    "C2H6OS", 1.1014, generic_name="DIMETHYL_SULFOXIDE", energies=ENERGIES, engine=ENGINE
)
ETHANE = Material("C2H6", 0.00125324, generic_name="ETHANE", energies=ENERGIES, engine=ENGINE)
ETHYL_ALCOHOL = Material(
    "C2H6O", 0.7893, generic_name="ETHYL_ALCOHOL", energies=ENERGIES, engine=ENGINE
)
ETHYL_CELLULOSE = Material(
    "H0.090027C0.585182O0.324791",
    1.13,
    generic_name="ETHYL_CELLULOSE",
    energies=ENERGIES,
    engine=ENGINE
)
ETHYLENE = Material("C2H4", 0.00117497, generic_name="ETHYLENE", energies=ENERGIES, engine=ENGINE)
EYE_LENS_ICRP = Material(
    "H0.096C0.195N0.057O0.646Na0.001P0.001S0.003Cl0.001",
    1.07,
    generic_name="EYE_LENS_ICRP",
    energies=ENERGIES,
    engine=ENGINE
)
FERRIC_OXIDE = Material("Fe2O3", 5.2, generic_name="FERRIC_OXIDE", energies=ENERGIES, engine=ENGINE)
FERROBORIDE = Material("FeB", 7.15, generic_name="FERROBORIDE", energies=ENERGIES, engine=ENGINE)
FERROUS_OXIDE = Material("FeO", 5.7, generic_name="FERROUS_OXIDE", energies=ENERGIES, engine=ENGINE)
FERROUS_SULFATE = Material(
    "H0.108259N2.7e-05O0.878636Na2.2e-05S0.012968Cl3.4e-05Fe5.4e-05",
    1.024,
    generic_name="FERROUS_SULFATE",
    energies=ENERGIES,
    engine=ENGINE
)
GADOLINIUM_OXYSULFIDE = Material(
    "Gd2O2S", 7.44, generic_name="GADOLINIUM_OXYSULFIDE", energies=ENERGIES, engine=ENGINE
)
GALLIUM_ARSENIDE = Material(
    "GaAs", 5.31, generic_name="GALLIUM_ARSENIDE", energies=ENERGIES, engine=ENGINE
)
GEL_PHOTO_EMULSION = Material(
    "H0.08118C0.41606N0.11124O0.38064S0.01088",
    1.2914,
    generic_name="GEL_PHOTO_EMULSION",
    energies=ENERGIES,
    engine=ENGINE
)
Pyrex_Glass = Material(
    "B0.0400639O0.539561Na0.0281909Al0.011644Si0.377219K0.00332099",
    2.23,
    generic_name="Pyrex_Glass",
    energies=ENERGIES,
    engine=ENGINE,
)
GLASS_LEAD = Material(
    "O0.156453Si0.080866Ti0.008092As0.002651Pb0.751938",
    6.22,
    generic_name="GLASS_LEAD",
    energies=ENERGIES,
    engine=ENGINE,
)
GLASS_PLATE = Material(
    "O0.4598Na0.0964411Si0.336553Ca0.107205",
    2.4,
    generic_name="GLASS_PLATE",
    energies=ENERGIES,
    engine=ENGINE,
)
GLUTAMINE = Material("C5H10N2O3", 1.46, generic_name="GLUTAMINE", energies=ENERGIES, engine=ENGINE)
GLYCEROL = Material("C3H8O3", 1.2613, generic_name="GLYCEROL", energies=ENERGIES, engine=ENGINE)
GUANINE = Material("C5H5N5O", 2.2, generic_name="GUANINE", energies=ENERGIES, engine=ENGINE)
GYPSUM = Material("CaSO6H4", 2.32, generic_name="GYPSUM", energies=ENERGIES, engine=ENGINE)
KAPTON = Material("C22H10N2O5", 1.42, generic_name="KAPTON", energies=ENERGIES, engine=ENGINE)
LANTHANUM_OXYBROMIDE = Material(
    "LaBrO", 6.28, generic_name="LANTHANUM_OXYBROMIDE", energies=ENERGIES, engine=ENGINE
)
LANTHANUM_OXYSULFIDE = Material(
    "La2O2S", 5.86, generic_name="LANTHANUM_OXYSULFIDE", energies=ENERGIES, engine=ENGINE
)
LEAD_OXIDE = Material(
    "O0.071682Pb0.928318", 9.53, generic_name="LEAD_OXIDE", energies=ENERGIES, engine=ENGINE
)
LITHIUM_AMIDE = Material("LiNH2", 1.178, generic_name="LITHIUM_AMIDE", energies=ENERGIES, engine=ENGINE)
LITHIUM_CARBONATE = Material(
    "Li2CO3", 2.11, generic_name="LITHIUM_CARBONATE", energies=ENERGIES, engine=ENGINE
)
LITHIUM_FLUORIDE = Material(
    "LiF", 2.635, generic_name="LITHIUM_FLUORIDE", energies=ENERGIES, engine=ENGINE
)
LITHIUM_HYDRIDE = Material(
    "LiH", 0.82, generic_name="LITHIUM_HYDRIDE", energies=ENERGIES, engine=ENGINE
)
LITHIUM_IODIDE = Material("LiI", 3.494, generic_name="LITHIUM_IODIDE", energies=ENERGIES, engine=ENGINE)
LITHIUM_OXIDE = Material("Li2O", 2.013, generic_name="LITHIUM_OXIDE", energies=ENERGIES, engine=ENGINE)
LITHIUM_TETRABORATE = Material(
    "Li2B4O7", 2.44, generic_name="LITHIUM_TETRABORATE", energies=ENERGIES, engine=ENGINE
)
LUNG_ICRP = Material(
    "H0.105C0.083N0.023O0.779Na0.002P0.001S0.002Cl0.003K0.002",
    1.04,
    generic_name="LUNG_ICRP",
    energies=ENERGIES,
    engine=ENGINE,
)
M3_WAX = Material(
    "H0.114318C0.655824O0.0921831Mg0.134792Ca0.002883",
    1.05,
    generic_name="M3_WAX",
    energies=ENERGIES,
    engine=ENGINE
)
MAGNESIUM_CARBONATE = Material(
    "MgCO3", 2.958, generic_name="MAGNESIUM_CARBONATE", energies=ENERGIES, engine=ENGINE
)
MAGNESIUM_FLUORIDE = Material(
    "MgF2", 3.0, generic_name="MAGNESIUM_FLUORIDE", energies=ENERGIES, engine=ENGINE
)
MAGNESIUM_OXIDE = Material(
    "MgO", 3.58, generic_name="MAGNESIUM_OXIDE", energies=ENERGIES, engine=ENGINE
)
MAGNESIUM_TETRABORATE = Material(
    "MgB4O7", 2.53, generic_name="MAGNESIUM_TETRABORATE", energies=ENERGIES, engine=ENGINE
)
MERCURIC_IODIDE = Material(
    "HgI2", 6.36, generic_name="MERCURIC_IODIDE", energies=ENERGIES, engine=ENGINE
)
METHANE = Material("CH4", 0.000667151, generic_name="METHANE", energies=ENERGIES, engine=ENGINE)
METHANOL = Material("CH4O", 0.7914, generic_name="METHANOL", energies=ENERGIES, engine=ENGINE)
MIX_D_WAX = Material(
    "H0.13404C0.77796O0.03502Mg0.038594Ti0.014386",
    0.99,
    generic_name="MIX_D_WAX",
    energies=ENERGIES,
    engine=ENGINE
)
MS20_TISSUE = Material(
    "H0.081192C0.583442N0.017798O0.186381Mg0.130287Cl0.0009",
    1.0,
    generic_name="MS20_TISSUE",
    energies=ENERGIES,
    engine=ENGINE
)
MUSCLE_SKELETAL_ICRP = Material(
    "H0.102C0.143N0.034O0.71Na0.001P0.002S0.003Cl0.001K0.004",
    1.05,
    generic_name="MUSCLE_SKELETAL_ICRP",
    energies=ENERGIES,
    engine=ENGINE
)
MUSCLE_STRIATED_ICRU = Material(
    "H0.102102C0.123123N0.035035O0.72973Na0.001001P0.002002S0.004004K0.003003",
    1.04,
    generic_name="MUSCLE_STRIATED_ICRU",
    energies=ENERGIES,
    engine=ENGINE
)
MUSCLE_WITH_SUCROSE = Material(
    "H0.0982341C0.156214N0.035451O0.710101",
    1.11,
    generic_name="MUSCLE_WITH_SUCROSE",
    energies=ENERGIES,
    engine=ENGINE
)
MUSCLE_WITHOUT_SUCROSE = Material(
    "H0.101969C0.120058N0.035451O0.742522",
    1.07,
    generic_name="MUSCLE_WITHOUT_SUCROSE",
    energies=ENERGIES,
    engine=ENGINE
)
NAPHTHALENE = Material("C10H8", 1.145, generic_name="NAPHTHALENE", energies=ENERGIES, engine=ENGINE)
NITROBENZENE = Material(
    "C6H5NO2", 1.19867, generic_name="NITROBENZENE", energies=ENERGIES, engine=ENGINE
)
NITROUS_OXIDE = Material(
    "N2O", 0.00183094, generic_name="NITROUS_OXIDE", energies=ENERGIES, engine=ENGINE
)
OCTANE = Material("C8H18", 0.7026, generic_name="OCTANE", energies=ENERGIES, engine=ENGINE)
PARAFFIN = Material("C25H52", 0.93, generic_name="PARAFFIN", energies=ENERGIES, engine=ENGINE)
PHOTO_EMULSION = Material(
    "H0.0141C0.072261N0.01932O0.066101S0.00189Br0.349103Ag0.474105I0.00312",
    3.815,
    generic_name="PHOTO_EMULSION",
    energies=ENERGIES,
    engine=ENGINE
)
PLASTIC_SC_VINYLTOLUENE = Material(
    "C9H10", 1.032, generic_name="PLASTIC_SC_VINYLTOLUENE", energies=ENERGIES, engine=ENGINE
)
PLUTONIUM_DIOXIDE = Material(
    "PuO2", 11.46, generic_name="PLUTONIUM_DIOXIDE", energies=ENERGIES, engine=ENGINE
)
POLYACRYLONITRILE = Material(
    "C3H3N", 1.17, generic_name="POLYACRYLONITRILE", energies=ENERGIES, engine=ENGINE
)
POLYCARBONATE = Material(
    "C16H14O3", 1.2, generic_name="POLYCARBONATE", energies=ENERGIES, engine=ENGINE
)
POLYCHLOROSTYRENE = Material(
    "C8H7Cl", 1.3, generic_name="POLYCHLOROSTYRENE", energies=ENERGIES, engine=ENGINE
)
POLYETHYLENE = Material("CH2", 0.94, generic_name="POLYETHYLENE", energies=ENERGIES, engine=ENGINE)
MYLAR = Material("C10H8O4", 1.4, generic_name="MYLAR", energies=ENERGIES, engine=ENGINE)
PLEXIGLASS = Material("C5H8O2", 1.19, generic_name="PLEXIGLASS", energies=ENERGIES, engine=ENGINE)
POLYOXYMETHYLENE = Material(
    "CH2O", 1.425, generic_name="POLYOXYMETHYLENE", energies=ENERGIES, engine=ENGINE
)
POLYPROPYLENE = Material("C2H4", 0.9, generic_name="POLYPROPYLENE", energies=ENERGIES, engine=ENGINE)
POLYSTYRENE = Material("C8H8", 1.06, generic_name="POLYSTYRENE", energies=ENERGIES, engine=ENGINE)
TEFLON = Material("C2F4", 2.2, generic_name="TEFLON", energies=ENERGIES, engine=ENGINE)
POLYTRIFLUOROCHLOROETHYLENE = Material(
    "C2F3Cl", 2.1, generic_name="POLYTRIFLUOROCHLOROETHYLENE", energies=ENERGIES, engine=ENGINE
)
POLYVINYL_ACETATE = Material(
    "C4H6O2", 1.19, generic_name="POLYVINYL_ACETATE", energies=ENERGIES, engine=ENGINE
)
POLYVINYL_ALCOHOL = Material(
    "C2H4O", 1.3, generic_name="POLYVINYL_ALCOHOL", energies=ENERGIES, engine=ENGINE
)
POLYVINYL_BUTYRAL = Material(
    "C8H14O2", 1.12, generic_name="POLYVINYL_BUTYRAL", energies=ENERGIES, engine=ENGINE
)
POLYVINYL_CHLORIDE = Material(
    "C2H3Cl", 1.3, generic_name="POLYVINYL_CHLORIDE", energies=ENERGIES, engine=ENGINE
)
POLYVINYLIDENE_CHLORIDE = Material(
    "C2H2Cl2", 1.7, generic_name="POLYVINYLIDENE_CHLORIDE", energies=ENERGIES, engine=ENGINE
)
POLYVINYLIDENE_FLUORIDE = Material(
    "C2H2F2", 1.76, generic_name="POLYVINYLIDENE_FLUORIDE", energies=ENERGIES, engine=ENGINE
)
POLYVINYL_PYRROLIDONE = Material(
    "C6H9NO", 1.25, generic_name="POLYVINYL_PYRROLIDONE", energies=ENERGIES, engine=ENGINE
)
POTASSIUM_IODIDE = Material(
    "KI", 3.13, generic_name="POTASSIUM_IODIDE", energies=ENERGIES, engine=ENGINE
)
POTASSIUM_OXIDE = Material(
    "K2O", 2.32, generic_name="POTASSIUM_OXIDE", energies=ENERGIES, engine=ENGINE
)
PROPANE = Material("C3H8", 0.00187939, generic_name="PROPANE", energies=ENERGIES, engine=ENGINE)
lPROPANE = Material("C3H8", 0.43, generic_name="lPROPANE", energies=ENERGIES, engine=ENGINE)
PYRIDINE = Material("C5H5N", 0.9819, generic_name="PYRIDINE", energies=ENERGIES, engine=ENGINE)
RUBBER_BUTYL = Material(
    "H0.143711C0.856289", 0.92, generic_name="RUBBER_BUTYL", energies=ENERGIES, engine=ENGINE
)
RUBBER_NATURAL = Material(
    "H0.118371C0.881629", 0.92, generic_name="RUBBER_NATURAL", energies=ENERGIES, engine=ENGINE
)
RUBBER_NEOPRENE = Material(
    "H0.05692C0.542646Cl0.400434",
    1.23,
    generic_name="RUBBER_NEOPRENE",
    energies=ENERGIES,
    engine=ENGINE
)
SILICON_DIOXIDE = Material(
    "SiO2", 2.32, generic_name="SILICON_DIOXIDE", energies=ENERGIES, engine=ENGINE
)
SILVER_BROMIDE = Material(
    "AgBr", 6.473, generic_name="SILVER_BROMIDE", energies=ENERGIES, engine=ENGINE
)
SILVER_CHLORIDE = Material(
    "AgCl", 5.56, generic_name="SILVER_CHLORIDE", energies=ENERGIES, engine=ENGINE
)
SILVER_HALIDES = Material(
    "Br0.422895Ag0.573748I0.003357",
    6.47,
    generic_name="SILVER_HALIDES",
    energies=ENERGIES,
    engine=ENGINE
)
SILVER_IODIDE = Material("AgI", 6.01, generic_name="SILVER_IODIDE", energies=ENERGIES, engine=ENGINE)
SKIN_ICRP = Material(
    "H0.1C0.204N0.042O0.645Na0.002P0.001S0.002Cl0.003K0.001",
    1.09,
    generic_name="SKIN_ICRP",
    energies=ENERGIES,
    engine=ENGINE
)
SODIUM_CARBONATE = Material(
    "Na2CO3", 2.532, generic_name="SODIUM_CARBONATE", energies=ENERGIES, engine=ENGINE
)
SODIUM_IODIDE = Material("NaI", 3.667, generic_name="SODIUM_IODIDE", energies=ENERGIES, engine=ENGINE)
SODIUM_MONOXIDE = Material(
    "Na2O", 2.27, generic_name="SODIUM_MONOXIDE", energies=ENERGIES, engine=ENGINE
)
SODIUM_NITRATE = Material(
    "NaNO3", 2.261, generic_name="SODIUM_NITRATE", energies=ENERGIES, engine=ENGINE
)
STILBENE = Material("C14H12", 0.9707, generic_name="STILBENE", energies=ENERGIES, engine=ENGINE)
SUCROSE = Material("C12H22O11", 1.5805, generic_name="SUCROSE", energies=ENERGIES, engine=ENGINE)
TERPHENYL = Material("C18H14", 1.24, generic_name="TERPHENYL", energies=ENERGIES, engine=ENGINE)
TESTIS_ICRP = Material(
    "H0.106C0.099N0.02O0.766Na0.002P0.001S0.002Cl0.002K0.002",
    1.04,
    generic_name="TESTIS_ICRP",
    energies=ENERGIES,
    engine=ENGINE
)
TETRACHLOROETHYLENE = Material(
    "C2Cl4", 1.625, generic_name="TETRACHLOROETHYLENE", energies=ENERGIES, engine=ENGINE
)
THALLIUM_CHLORIDE = Material(
    "TlCl", 7.004, generic_name="THALLIUM_CHLORIDE", energies=ENERGIES, engine=ENGINE
)
TISSUE_SOFT_ICRP = Material(
    "H0.105C0.256N0.027O0.602Na0.001P0.002S0.003Cl0.002K0.002",
    1.03,
    generic_name="TISSUE_SOFT_ICRP",
    energies=ENERGIES,
    engine=ENGINE
)
TITANIUM_DIOXIDE = Material(
    "TiO2", 4.26, generic_name="TITANIUM_DIOXIDE", energies=ENERGIES, engine=ENGINE
)
TOLUENE = Material("C7H8", 0.8669, generic_name="TOLUENE", energies=ENERGIES, engine=ENGINE)
TRICHLOROETHYLENE = Material(
    "C2HCl3", 1.46, generic_name="TRICHLOROETHYLENE", energies=ENERGIES, engine=ENGINE
)
TRIETHYL_PHOSPHATE = Material(
    "C6H15O4P", 1.07, generic_name="TRIETHYL_PHOSPHATE", energies=ENERGIES, engine=ENGINE
)
TUNGSTEN_HEXAFLUORIDE = Material(
    "WF6", 2.4, generic_name="TUNGSTEN_HEXAFLUORIDE", energies=ENERGIES, engine=ENGINE
)
URANIUM_DICARBIDE = Material(
    "UC2", 11.28, generic_name="URANIUM_DICARBIDE", energies=ENERGIES, engine=ENGINE
)
URANIUM_MONOCARBIDE = Material(
    "UC", 13.63, generic_name="URANIUM_MONOCARBIDE", energies=ENERGIES, engine=ENGINE
)
URANIUM_OXIDE = Material("UO2", 10.96, generic_name="URANIUM_OXIDE", energies=ENERGIES, engine=ENGINE)
UREA = Material("CH4N2O", 1.323, generic_name="UREA", energies=ENERGIES, engine=ENGINE)
VALINE = Material("C5H11NO2", 1.23, generic_name="VALINE", energies=ENERGIES, engine=ENGINE)
VITON = Material(
    "H0.009417C0.280555F0.710028", 1.8, generic_name="VITON", energies=ENERGIES, engine=ENGINE
)
WATER = Material("H2O", 1.0, generic_name="WATER", energies=ENERGIES, engine=ENGINE)
WATER_VAPOR = Material("H2O", 0.000756182, generic_name="WATER_VAPOR", energies=ENERGIES, engine=ENGINE)
XYLENE = Material("C8H10", 0.87, generic_name="XYLENE", energies=ENERGIES, engine=ENGINE)
GRAPHITE = Material("C", 2.21, generic_name="GRAPHITE", energies=ENERGIES, engine=ENGINE)
# endregion - NIST Compounds

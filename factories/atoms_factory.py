from PenguinMol3D.general.globals import ELEMENT_COLORS
from PenguinMol3D.geometries.atoms.atoms_geometry import (
    HydrogenGeometry,
    HeliumGeometry,
    LithiumGeometry,
    BerylliumGeometry,
    BoronGeometry,
    CarbonGeometry,
    NitrogenGeometry,
    OxygenGeometry,
    FluorineGeometry,
    NeonGeometry,
    SodiumGeometry,
    MagnesiumGeometry,
    AluminumGeometry,
    SiliconGeometry,
    PhosphorusGeometry,
    SulfurGeometry,
    ChlorineGeometry,
    ArgonGeometry,
    PotassiumGeometry,
    CalciumGeometry,
    ScandiumGeometry,
    TitaniumGeometry,
    VanadiumGeometry,
    ChromiumGeometry,
    ManganeseGeometry,
    IronGeometry,
    CobaltGeometry,
    NickelGeometry,
    CopperGeometry,
    ZincGeometry,
    GalliumGeometry,
    GermaniumGeometry,
    ArsenicGeometry,
    SeleniumGeometry,
    BromineGeometry,
    KryptonGeometry,
    RubidiumGeometry,
    StrontiumGeometry,
    YttriumGeometry,
    ZirconiumGeometry,
    NiobiumGeometry,
    MolybdenumGeometry,
    TechnetiumGeometry,
    RutheniumGeometry,
    RhodiumGeometry,
    PalladiumGeometry,
    SilverGeometry,
    CadmiumGeometry,
    IndiumGeometry,
    TinGeometry,
    AntimonyGeometry,
    TelluriumGeometry,
    IodineGeometry,
    XenonGeometry,
    CaesiumGeometry,
    BariumGeometry,
    LanthanumGeometry,
    CeriumGeometry,
    PraseodymiumGeometry,
    NeodymiumGeometry,
    PromethiumGeometry,
    SamariumGeometry,
    EuropiumGeometry,
    GadoliniumGeometry,
    TerbiumGeometry,
    DysprosiumGeometry,
    HolmiumGeometry,
    ErbiumGeometry,
    ThuliumGeometry,
    YtterbiumGeometry,
    LutetiumGeometry,
    HafniumGeometry,
    TantalumGeometry,
    TungstenGeometry,
    RheniumGeometry,
    OsmiumGeometry,
    IridiumGeometry,
    PlatinumGeometry,
    GoldGeometry,
    MercuryGeometry,
    ThalliumGeometry,
    BismuthGeometry,
    PoloniumGeometry,
    AstatineGeometry,
    RadonGeometry,
    FranciumGeometry,
    RadiumGeometry,
    ActiniumGeometry,
    ThoriumGeometry,
    ProtactiniumGeometry,
    UraniumGeometry,
    NeptuniumGeometry,
    PlutoniumGeometry,
    AmericiumGeometry,
    CuriumGeometry,
    BerkeliumGeometry,
    CaliforniumGeometry,
    EinsteiniumGeometry
)

from PenguinMol3D.factories.base_factory import BaseFactory
from PenguinMol3D.objects.mesh import Mesh


class Atom3D(Mesh):
    def __init__(self, geometry, material):
        self._instances = []
        Mesh.__init__(self, geometry, material)

    def get_instances(self) -> list:
        return self._instances

    def add_instance(self, instance):
        self._instances.append(instance)
        name = f"model_matrix[{len(self._instances)-1}]"
        self.material.add_uniform(instance, "mat4", name)
        self.material.locate_uniform(name)

class AtomsFactory(BaseFactory):
    def __init__(self, material_type: str = "rubber"):
        BaseFactory.__init__(self, material_type=material_type)
        self._atoms_parameters = {}

    def get_atom_3d(self, atom_symbol: str) -> Atom3D:
        atom_3d = None

        if atom_symbol not in self._atoms_parameters:
            material = self.material_type(properties={"base_color": ELEMENT_COLORS[atom_symbol],
                                                      "use_instanced_rendering" : True})
            material.settings["cull_face"] = True
            material.settings["back_side"] = False
            if   atom_symbol == "H":
                self._atoms_parameters[atom_symbol] = (HydrogenGeometry(), material)
            elif atom_symbol == "He":
                self._atoms_parameters[atom_symbol] = (HeliumGeometry(), material)
            elif atom_symbol == "Li":
                self._atoms_parameters[atom_symbol] = (LithiumGeometry(), material)
            elif atom_symbol == "Be":
                self._atoms_parameters[atom_symbol] = (BerylliumGeometry(), material)
            elif atom_symbol == "B":
                self._atoms_parameters[atom_symbol] = (BoronGeometry(), material)
            elif atom_symbol == "C":
                self._atoms_parameters[atom_symbol] = (CarbonGeometry(), material)
            elif atom_symbol == "N":
                self._atoms_parameters[atom_symbol] = (NitrogenGeometry(), material)
            elif atom_symbol == "O":
                self._atoms_parameters[atom_symbol] = (OxygenGeometry(), material)
            elif atom_symbol == "F":
                self._atoms_parameters[atom_symbol] = (FluorineGeometry(), material)
            elif atom_symbol == "Ne":
                self._atoms_parameters[atom_symbol] = (NeonGeometry(), material)
            elif atom_symbol == "Na":
                self._atoms_parameters[atom_symbol] = (SodiumGeometry(), material)
            elif atom_symbol == "Mg":
                self._atoms_parameters[atom_symbol] = (MagnesiumGeometry(), material)
            elif atom_symbol == "Al":
                self._atoms_parameters[atom_symbol] = (AluminumGeometry(), material)
            elif atom_symbol == "Si":
                self._atoms_parameters[atom_symbol] = (SiliconGeometry(), material)
            elif atom_symbol == "P":
                self._atoms_parameters[atom_symbol] = (PhosphorusGeometry(), material)
            elif atom_symbol == "S":
                self._atoms_parameters[atom_symbol] = (SulfurGeometry(), material)
            elif atom_symbol == "Cl":
                self._atoms_parameters[atom_symbol] = (ChlorineGeometry(), material)
            elif atom_symbol == "Ar":
                self._atoms_parameters[atom_symbol] = (ArgonGeometry(), material)
            elif atom_symbol == "K":
                self._atoms_parameters[atom_symbol] = (PotassiumGeometry(), material)
            elif atom_symbol == "Ca":
                self._atoms_parameters[atom_symbol] = (CalciumGeometry(), material)
            elif atom_symbol == "Sc":
                self._atoms_parameters[atom_symbol] = (ScandiumGeometry(), material)
            elif atom_symbol == "Ti":
                self._atoms_parameters[atom_symbol] = (TitaniumGeometry(), material)
            elif atom_symbol == "V":
                self._atoms_parameters[atom_symbol] = (VanadiumGeometry(), material)
            elif atom_symbol == "Cr":
                self._atoms_parameters[atom_symbol] = (ChromiumGeometry(), material)
            elif atom_symbol == "Mn":
                self._atoms_parameters[atom_symbol] = (ManganeseGeometry(), material)
            elif atom_symbol == "Fe":
                self._atoms_parameters[atom_symbol] = (IronGeometry(), material)
            elif atom_symbol == "Co":
                self._atoms_parameters[atom_symbol] = (CobaltGeometry(), material)
            elif atom_symbol == "Ni":
                self._atoms_parameters[atom_symbol] = (NickelGeometry(), material)
            elif atom_symbol == "Cu":
                self._atoms_parameters[atom_symbol] = (CopperGeometry(), material)
            elif atom_symbol == "Zn":
                self._atoms_parameters[atom_symbol] = (ZincGeometry(), material)
            elif atom_symbol == "Ga":
                self._atoms_parameters[atom_symbol] = (GalliumGeometry(), material)
            elif atom_symbol == "Ge":
                self._atoms_parameters[atom_symbol] = (GermaniumGeometry(), material)
            elif atom_symbol == "As":
                self._atoms_parameters[atom_symbol] = (ArsenicGeometry(), material)
            elif atom_symbol == "Se":
                self._atoms_parameters[atom_symbol] = (SeleniumGeometry(), material)
            elif atom_symbol == "Br":
                self._atoms_parameters[atom_symbol] = (BromineGeometry(), material)
            elif atom_symbol == "Kr":
                self._atoms_parameters[atom_symbol] = (KryptonGeometry(), material)
            elif atom_symbol == "Rb":
                self._atoms_parameters[atom_symbol] = (RubidiumGeometry(), material)
            elif atom_symbol == "Sr":
                self._atoms_parameters[atom_symbol] = (StrontiumGeometry(), material)
            elif atom_symbol == "Y":
                self._atoms_parameters[atom_symbol] = (YttriumGeometry(), material)
            elif atom_symbol == "Zr":
                self._atoms_parameters[atom_symbol] = (ZirconiumGeometry(), material)
            elif atom_symbol == "Nb":
                self._atoms_parameters[atom_symbol] = (NiobiumGeometry(), material)
            elif atom_symbol == "Mo":
                self._atoms_parameters[atom_symbol] = (MolybdenumGeometry(), material)
            elif atom_symbol == "Tc":
                self._atoms_parameters[atom_symbol] = (TechnetiumGeometry(), material)
            elif atom_symbol == "Ru":
                self._atoms_parameters[atom_symbol] = (RutheniumGeometry(), material)
            elif atom_symbol == "Rh":
                self._atoms_parameters[atom_symbol] = (RhodiumGeometry(), material)
            elif atom_symbol == "Pd":
                self._atoms_parameters[atom_symbol] = (PalladiumGeometry(), material)
            elif atom_symbol == "Ag":
                self._atoms_parameters[atom_symbol] = (SilverGeometry(), material)
            elif atom_symbol == "Cd":
                self._atoms_parameters[atom_symbol] = (CadmiumGeometry(), material)
            elif atom_symbol == "In":
                self._atoms_parameters[atom_symbol] = (IndiumGeometry(), material)
            elif atom_symbol == "Sn":
                self._atoms_parameters[atom_symbol] = (TinGeometry(), material)
            elif atom_symbol == "Sb":
                self._atoms_parameters[atom_symbol] = (AntimonyGeometry(), material)
            elif atom_symbol == "Te":
                self._atoms_parameters[atom_symbol] = (TelluriumGeometry(), material)
            elif atom_symbol == "I":
                self._atoms_parameters[atom_symbol] = (IodineGeometry(), material)
            elif atom_symbol == "Xe":
                self._atoms_parameters[atom_symbol] = (XenonGeometry(), material)
            elif atom_symbol == "Cs":
                self._atoms_parameters[atom_symbol] = (CaesiumGeometry(), material)
            elif atom_symbol == "Ba":
                self._atoms_parameters[atom_symbol] = (BariumGeometry(), material)
            elif atom_symbol == "La":
                self._atoms_parameters[atom_symbol] = (LanthanumGeometry(), material)
            elif atom_symbol == "Ce":
                self._atoms_parameters[atom_symbol] = (CeriumGeometry(), material)
            elif atom_symbol == "Pr":
                self._atoms_parameters[atom_symbol] = (PraseodymiumGeometry(), material)
            elif atom_symbol == "Nd":
                self._atoms_parameters[atom_symbol] = (NeodymiumGeometry(), material)
            elif atom_symbol == "Pm":
                self._atoms_parameters[atom_symbol] = (PromethiumGeometry(), material)
            elif atom_symbol == "Sm":
                self._atoms_parameters[atom_symbol] = (SamariumGeometry(), material)
            elif atom_symbol == "Eu":
                self._atoms_parameters[atom_symbol] = (EuropiumGeometry(), material)
            elif atom_symbol == "Gd":
                self._atoms_parameters[atom_symbol] = (GadoliniumGeometry(), material)
            elif atom_symbol == "Tb":
                self._atoms_parameters[atom_symbol] = (TerbiumGeometry(), material)
            elif atom_symbol == "Dy":
                self._atoms_parameters[atom_symbol] = (DysprosiumGeometry(), material)
            elif atom_symbol == "Ho":
                self._atoms_parameters[atom_symbol] = (HolmiumGeometry(), material)
            elif atom_symbol == "Er":
                self._atoms_parameters[atom_symbol] = (ErbiumGeometry(), material)
            elif atom_symbol == "Th":
                self._atoms_parameters[atom_symbol] = (ThuliumGeometry(), material)
            elif atom_symbol == "Yb":
                self._atoms_parameters[atom_symbol] = (YtterbiumGeometry(), material)
            elif atom_symbol == "Lu":
                self._atoms_parameters[atom_symbol] = (LutetiumGeometry(), material)
            elif atom_symbol == "Hf":
                self._atoms_parameters[atom_symbol] = (HafniumGeometry(), material)
            elif atom_symbol == "Ta":
                self._atoms_parameters[atom_symbol] = (TantalumGeometry(), material)
            elif atom_symbol == "W":
                self._atoms_parameters[atom_symbol] = (TungstenGeometry(), material)
            elif atom_symbol == "Re":
                self._atoms_parameters[atom_symbol] = (RheniumGeometry(), material)
            elif atom_symbol == "Os":
                self._atoms_parameters[atom_symbol] = (OsmiumGeometry(), material)
            elif atom_symbol == "Ir":
                self._atoms_parameters[atom_symbol] = (IridiumGeometry(), material)
            elif atom_symbol == "Pt":
                self._atoms_parameters[atom_symbol] = (PlatinumGeometry(), material)
            elif atom_symbol == "Au":
                self._atoms_parameters[atom_symbol] = (GoldGeometry(), material)
            elif atom_symbol == "Hg":
                self._atoms_parameters[atom_symbol] = (MercuryGeometry(), material)
            elif atom_symbol == "Tl":
                self._atoms_parameters[atom_symbol] = (ThalliumGeometry(), material)
            elif atom_symbol == "Bi":
                self._atoms_parameters[atom_symbol] = (BismuthGeometry(), material)
            elif atom_symbol == "Po":
                self._atoms_parameters[atom_symbol] = (PoloniumGeometry(), material)
            elif atom_symbol == "At":
                self._atoms_parameters[atom_symbol] = (AstatineGeometry(), material)
            elif atom_symbol == "Rn":
                self._atoms_parameters[atom_symbol] = (RadonGeometry(), material)
            elif atom_symbol == "Fr":
                self._atoms_parameters[atom_symbol] = (FranciumGeometry(), material)
            elif atom_symbol == "Ra":
                self._atoms_parameters[atom_symbol] = (RadiumGeometry(), material)
            elif atom_symbol == "Ac":
                self._atoms_parameters[atom_symbol] = (ActiniumGeometry(), material)
            elif atom_symbol == "Th":
                self._atoms_parameters[atom_symbol] = (ThoriumGeometry(), material)
            elif atom_symbol == "Pa":
                self._atoms_parameters[atom_symbol] = (ProtactiniumGeometry(), material)
            elif atom_symbol == "U":
                self._atoms_parameters[atom_symbol] = (UraniumGeometry(), material)
            elif atom_symbol == "Np":
                self._atoms_parameters[atom_symbol] = (NeptuniumGeometry(), material)
            elif atom_symbol == "Pu":
                self._atoms_parameters[atom_symbol] = (PlutoniumGeometry(), material)
            elif atom_symbol == "Am":
                self._atoms_parameters[atom_symbol] = (AmericiumGeometry(), material)
            elif atom_symbol == "Cm":
                self._atoms_parameters[atom_symbol] = (CuriumGeometry(), material)
            elif atom_symbol == "Bk":
                self._atoms_parameters[atom_symbol] = (BerkeliumGeometry(), material)
            elif atom_symbol == "Cf":
                self._atoms_parameters[atom_symbol] = (CaliforniumGeometry(), material)
            elif atom_symbol == "Es":
                self._atoms_parameters[atom_symbol] = (EinsteiniumGeometry(), material)

        atom_3d = Atom3D(*self._atoms_parameters[atom_symbol])
        return atom_3d






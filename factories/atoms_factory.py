import numpy as np

from general.globals import ELEMENT_COLORS
from geometries.atoms import (
    hydrogen_geometry,
    helium_geometry,
    lithium_geometry,
    beryllium_geometry,
    boron_geometry,
    carbon_geometry,
    nitrogen_geometry,
    oxygen_geometry,
    fluorine_geometry,
    neon_geometry,
    sodium_geometry,
    magnesium_geometry,
    aluminum_geometry,
    silicon_geometry,
    phosphorus_geometry,
    sulfur_geometry,
    chlorine_geometry,
    argon_geometry,
    potassium_geometry,
    calcium_geometry,
    scandium_geometry,
    titanium_geometry,
    vanadium_geometry,
    manganese_geometry,
    iron_geometry,
    cobalt_geometry,
    nickel_geometry,
    copper_geometry,
    zinc_geometry,
    gallium_geometry,
    germanium_geometry,
    arsenic_geometry,
    selenium_geometry,
    bromine_geometry,
    krypton_geometry,
    rubidium_geometry,
    strontium_geometry,
    yttrium_geometry,
    zirconium_geometry,
    niobium_geometry,
    molybdenum_geometry,
    technetium_geometry,
    ruthenium_geometry,
    rhodium_geometry,
    palladium_geometry,
    silver_geometry,
    cadmium_geometry,
    indium_geometry,
    tin_geometry,
    antimony_geometry,
    tellurium_geometry,
    iodine_geometry,
    xenon_geometry,
    caesium_geometry,
    barium_geometry,
    lanthanum_geometry,
    cerium_geometry,
    praseodymium_geometry,
    neodymium_geometry,
    promethium_geometry,
    samarium_geometry,
    europium_geometry,
    gadolinium_geometry,
    terbium_geometry,
    dysprosium_geometry,
    holmium_geometry,
    erbium_geometry,
    thulium_geometry,
    ytterbium_geometry,
    lutetium_geometry,
    hafnium_geometry,
    tantalum_geometry,
    tungsten_geometry,
    rhenium_geometry,
    osmium_geometry,
    irirdium_geometry,
    platinum_geometry,
    gold_geometry,
    mercury_geometry,
    thallium_geometry,
    lead_geometry,
    bismuth_geometry,
    polonium_geometry,
    astatine_geometry,
    radon_geometry,
    francium_geometry,
    radium_geometry,
    actinium_geometry,
    thorium_geometry,
    protactinium_geometry,
    uranium_geometry,
    neptunium_geometry,
    plutonium_geometry,
    americium_geometry,
    curium_geometry,
    berkelium_geometry,
    californium_geometry,
    einsteinium_geometry
)

from materials.atom_phong_material import PhongMaterial
from objects.mesh import Mesh

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

class AtomsFactory:
    def __init__(self):
        self._atoms_parameters = {}

    def get_atom_3d(self, atom_symbol: str) -> Atom3D:
        atom_3d = None

        if atom_symbol not in self._atoms_parameters:
            material = PhongMaterial(properties={"base_color": ELEMENT_COLORS[atom_symbol]})
            material.settings["cull_face"] = True
            material.settings["back_side"] = False
            if   atom_symbol == "H":
                self._atoms_parameters[atom_symbol] = (hydrogen_geometry.HydrogenGeometry(), material)
            elif atom_symbol == "He":
                self._atoms_parameters[atom_symbol] = (helium_geometry.HeliumGeometry(), material)
            elif atom_symbol == "Li":
                self._atoms_parameters[atom_symbol] = (lithium_geometry.LithiumGeometry(), material)
            elif atom_symbol == "Be":
                self._atoms_parameters[atom_symbol] = (beryllium_geometry.BerylliumGeometry(), material)
            elif atom_symbol == "B":
                self._atoms_parameters[atom_symbol] = (boron_geometry.BoronGeometry(), material)
            elif atom_symbol == "C":
                self._atoms_parameters[atom_symbol] = (carbon_geometry.CarbonGeometry(), material)
            elif atom_symbol == "N":
                self._atoms_parameters[atom_symbol] = (nitrogen_geometry.NitrogenGeometry(), material)
            elif atom_symbol == "O":
                self._atoms_parameters[atom_symbol] = (oxygen_geometry.OxygenGeometry(), material)
            elif atom_symbol == "F":
                self._atoms_parameters[atom_symbol] = (fluorine_geometry.FluorineGeometry(), material)
            elif atom_symbol == "Ne":
                self._atoms_parameters[atom_symbol] = (neon_geometry.NeonGeometry(), material)
            elif atom_symbol == "Na":
                self._atoms_parameters[atom_symbol] = (sodium_geometry.SodiumGeometry(), material)
            elif atom_symbol == "Mg":
                self._atoms_parameters[atom_symbol] = (magnesium_geometry.MagnesiumGeometry(), material)
            elif atom_symbol == "Al":
                self._atoms_parameters[atom_symbol] = (aluminum_geometry.AluminumGeometry(), material)
            elif atom_symbol == "Si":
                self._atoms_parameters[atom_symbol] = (silicon_geometry.SiliconGeometry(), material)
            elif atom_symbol == "P":
                self._atoms_parameters[atom_symbol] = (phosphorus_geometry.PhosphorusGeometry(), material)
            elif atom_symbol == "S":
                self._atoms_parameters[atom_symbol] = (sulfur_geometry.SulfurGeometry(), material)
            elif atom_symbol == "Cl":
                self._atoms_parameters[atom_symbol] = (chlorine_geometry.ChlorineGeometry(), material)
            elif atom_symbol == "Ar":
                self._atoms_parameters[atom_symbol] = (argon_geometry.ArgonGeometry(), material)
            elif atom_symbol == "K":
                self._atoms_parameters[atom_symbol] = (potassium_geometry.PotassiumGeometry(), material)
            elif atom_symbol == "Ca":
                self._atoms_parameters[atom_symbol] = (calcium_geometry.CalciumGeometry(), material)
            elif atom_symbol == "Sc":
                self._atoms_parameters[atom_symbol] = (scandium_geometry.ScandiumGeometry(), material)
            elif atom_symbol == "Ti":
                self._atoms_parameters[atom_symbol] = (titanium_geometry.TitaniumGeometry(), material)
            elif atom_symbol == "V":
                self._atoms_parameters[atom_symbol] = (vanadium_geometry.VanadiumGeometry(), material)
            elif atom_symbol == "Cr":
                self._atoms_parameters[atom_symbol] = (vanadium_geometry.ChromiumGeometry(), material)
            elif atom_symbol == "Mn":
                self._atoms_parameters[atom_symbol] = (manganese_geometry.ManganeseGeometry(), material)
            elif atom_symbol == "Fe":
                self._atoms_parameters[atom_symbol] = (iron_geometry.IronGeometry(), material)
            elif atom_symbol == "Co":
                self._atoms_parameters[atom_symbol] = (cobalt_geometry.CobaltGeometry(), material)
            elif atom_symbol == "Ni":
                self._atoms_parameters[atom_symbol] = (nickel_geometry.NickelGeometry(), material)
            elif atom_symbol == "Cu":
                self._atoms_parameters[atom_symbol] = (copper_geometry.CopperGeometry(), material)
            elif atom_symbol == "Zn":
                self._atoms_parameters[atom_symbol] = (zinc_geometry.ZincGeometry(), material)
            elif atom_symbol == "Ga":
                self._atoms_parameters[atom_symbol] = (gallium_geometry.GalliumGeometry(), material)
            elif atom_symbol == "Ge":
                self._atoms_parameters[atom_symbol] = (germanium_geometry.GermaniumGeometry(), material)
            elif atom_symbol == "As":
                self._atoms_parameters[atom_symbol] = (arsenic_geometry.ArsenicGeometry(), material)
            elif atom_symbol == "Se":
                self._atoms_parameters[atom_symbol] = (selenium_geometry.SeleniumGeometry(), material)
            elif atom_symbol == "Br":
                self._atoms_parameters[atom_symbol] = (bromine_geometry.BromineGeometry(), material)
            elif atom_symbol == "Kr":
                self._atoms_parameters[atom_symbol] = (krypton_geometry.KryptonGeometry(), material)
            elif atom_symbol == "Rb":
                self._atoms_parameters[atom_symbol] = (rubidium_geometry.RubidiumGeometry(), material)
            elif atom_symbol == "Sr":
                self._atoms_parameters[atom_symbol] = (strontium_geometry.StrontiumGeometry(), material)
            elif atom_symbol == "Y":
                self._atoms_parameters[atom_symbol] = (yttrium_geometry.YttriumGeometry(), material)
            elif atom_symbol == "Zr":
                self._atoms_parameters[atom_symbol] = (zirconium_geometry.ZirconiumGeometry(), material)
            elif atom_symbol == "Nb":
                self._atoms_parameters[atom_symbol] = (niobium_geometry.NiobiumGeometry(), material)
            elif atom_symbol == "Mo":
                self._atoms_parameters[atom_symbol] = (molybdenum_geometry.MolybdenumGeometry(), material)
            elif atom_symbol == "Tc":
                self._atoms_parameters[atom_symbol] = (technetium_geometry.TechnetiumGeometry(), material)
            elif atom_symbol == "Ru":
                self._atoms_parameters[atom_symbol] = (ruthenium_geometry.RutheniumGeometry(), material)
            elif atom_symbol == "Rh":
                self._atoms_parameters[atom_symbol] = (rhodium_geometry.RhodiumGeometry(), material)
            elif atom_symbol == "Pd":
                self._atoms_parameters[atom_symbol] = (palladium_geometry.PalladiumGeometry(), material)
            elif atom_symbol == "Ag":
                self._atoms_parameters[atom_symbol] = (silver_geometry.SilverGeometry(), material)
            elif atom_symbol == "Cd":
                self._atoms_parameters[atom_symbol] = (cadmium_geometry.CadmiumGeometry(), material)
            elif atom_symbol == "In":
                self._atoms_parameters[atom_symbol] = (indium_geometry.IndiumGeometry(), material)
            elif atom_symbol == "Sn":
                self._atoms_parameters[atom_symbol] = (tin_geometry.TinGeometry(), material)
            elif atom_symbol == "Sb":
                self._atoms_parameters[atom_symbol] = (antimony_geometry.AntimonyGeometry(), material)
            elif atom_symbol == "Te":
                self._atoms_parameters[atom_symbol] = (tellurium_geometry.TelluriumGeometry(), material)
            elif atom_symbol == "I":
                self._atoms_parameters[atom_symbol] = (iodine_geometry.IodineGeometry(), material)
            elif atom_symbol == "Xe":
                self._atoms_parameters[atom_symbol] = (xenon_geometry.XenonGeometry(), material)
            elif atom_symbol == "Cs":
                self._atoms_parameters[atom_symbol] = (caesium_geometry.CaesiumGeometry(), material)
            elif atom_symbol == "Ba":
                self._atoms_parameters[atom_symbol] = (barium_geometry.BariumGeometry(), material)
            elif atom_symbol == "La":
                self._atoms_parameters[atom_symbol] = (lanthanum_geometry.LanthanumGeometry(), material)
            elif atom_symbol == "Ce":
                self._atoms_parameters[atom_symbol] = (cerium_geometry.CeriumGeometry(), material)
            elif atom_symbol == "Pr":
                self._atoms_parameters[atom_symbol] = (praseodymium_geometry.PraseodymiumGeometry(), material)
            elif atom_symbol == "Nd":
                self._atoms_parameters[atom_symbol] = (neodymium_geometry.NeodymiumGeometry(), material)
            elif atom_symbol == "Pm":
                self._atoms_parameters[atom_symbol] = (promethium_geometry.PromethiumGeometry(), material)
            elif atom_symbol == "Sm":
                self._atoms_parameters[atom_symbol] = (samarium_geometry.SamariumGeometry(), material)
            elif atom_symbol == "Eu":
                self._atoms_parameters[atom_symbol] = (europium_geometry.EuropiumGeometry(), material)
            elif atom_symbol == "Gd":
                self._atoms_parameters[atom_symbol] = (gadolinium_geometry.GadoliniumGeometry(), material)
            elif atom_symbol == "Tb":
                self._atoms_parameters[atom_symbol] = (terbium_geometry.TerbiumGeometry(), material)
            elif atom_symbol == "Dy":
                self._atoms_parameters[atom_symbol] = (dysprosium_geometry.DysprosiumGeometry(), material)
            elif atom_symbol == "Ho":
                self._atoms_parameters[atom_symbol] = (holmium_geometry.HolmiumGeometry(), material)
            elif atom_symbol == "Er":
                self._atoms_parameters[atom_symbol] = (erbium_geometry.ErbiumGeometry(), material)
            elif atom_symbol == "Th":
                self._atoms_parameters[atom_symbol] = (thulium_geometry.ErbiumGeometry(), material)
            elif atom_symbol == "Yb":
                self._atoms_parameters[atom_symbol] = (ytterbium_geometry.YtterbiumGeometry(), material)
            elif atom_symbol == "Lu":
                self._atoms_parameters[atom_symbol] = (lutetium_geometry.LutetiumGeometry(), material)
            elif atom_symbol == "Hf":
                self._atoms_parameters[atom_symbol] = (hafnium_geometry.HafniumGeometry(), material)
            elif atom_symbol == "Ta":
                self._atoms_parameters[atom_symbol] = (tantalum_geometry.TantalumGeometry(), material)
            elif atom_symbol == "W":
                self._atoms_parameters[atom_symbol] = (tungsten_geometry.TungstenGeometry(), material)
            elif atom_symbol == "Re":
                self._atoms_parameters[atom_symbol] = (rhenium_geometry.RheniumGeometry(), material)
            elif atom_symbol == "Os":
                self._atoms_parameters[atom_symbol] = (osmium_geometry.OsmiumGeometry(), material)
            elif atom_symbol == "Ir":
                self._atoms_parameters[atom_symbol] = (irirdium_geometry.IridiumGeometry(), material)
            elif atom_symbol == "Pt":
                self._atoms_parameters[atom_symbol] = (platinum_geometry.PlatinumGeometry(), material)
            elif atom_symbol == "Au":
                self._atoms_parameters[atom_symbol] = (gold_geometry.GoldGeometry(), material)
            elif atom_symbol == "Hg":
                self._atoms_parameters[atom_symbol] = (mercury_geometry.MercuryGeometry(), material)
            elif atom_symbol == "Tl":
                self._atoms_parameters[atom_symbol] = (thallium_geometry.ThalliumGeometry(), material)
            elif atom_symbol == "Bi":
                self._atoms_parameters[atom_symbol] = (bismuth_geometry.BismuthGeometry(), material)
            elif atom_symbol == "Po":
                self._atoms_parameters[atom_symbol] = (polonium_geometry.PoloniumGeometry(), material)
            elif atom_symbol == "At":
                self._atoms_parameters[atom_symbol] = (astatine_geometry.AstatineGeometry(), material)
            elif atom_symbol == "Rn":
                self._atoms_parameters[atom_symbol] = (radon_geometry.RadonGeometry(), material)
            elif atom_symbol == "Fr":
                self._atoms_parameters[atom_symbol] = (francium_geometry.FranciumGeometry(), material)
            elif atom_symbol == "Ra":
                self._atoms_parameters[atom_symbol] = (radium_geometry.RadiumGeometry(), material)
            elif atom_symbol == "Ac":
                self._atoms_parameters[atom_symbol] = (actinium_geometry.ActiniumGeometry(), material)
            elif atom_symbol == "Th":
                self._atoms_parameters[atom_symbol] = (thorium_geometry.ThoriumGeometry(), material)
            elif atom_symbol == "Pa":
                self._atoms_parameters[atom_symbol] = (protactinium_geometry.ProtactiniumGeometry(), material)
            elif atom_symbol == "U":
                self._atoms_parameters[atom_symbol] = (uranium_geometry.UraniumGeometry(), material)
            elif atom_symbol == "Np":
                self._atoms_parameters[atom_symbol] = (neptunium_geometry.NeptuniumGeometry(), material)
            elif atom_symbol == "Pu":
                self._atoms_parameters[atom_symbol] = (plutonium_geometry.PlutoniumGeometry(), material)
            elif atom_symbol == "Am":
                self._atoms_parameters[atom_symbol] = (americium_geometry.AmericiumGeometry(), material)
            elif atom_symbol == "Cm":
                self._atoms_parameters[atom_symbol] = (curium_geometry.CuriumGeometry(), material)
            elif atom_symbol == "Bk":
                self._atoms_parameters[atom_symbol] = (berkelium_geometry.BerkeliumGeometry(), material)
            elif atom_symbol == "Cf":
                self._atoms_parameters[atom_symbol] = (californium_geometry.CaliforniumGeometry(), material)
            elif atom_symbol == "Es":
                self._atoms_parameters[atom_symbol] = (einsteinium_geometry.EinsteiniumGeometry(), material)

        atom_3d = Atom3D(*self._atoms_parameters[atom_symbol])
        return atom_3d






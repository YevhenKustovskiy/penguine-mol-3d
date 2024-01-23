from general.globals import ELEMENT_COLOR
from geometries.atoms import (
    hydrogen_geometry,
    carbon_geometry,
    nitrogen_geometry,
    oxygen_geometry,
    iodine_geometry
)

from materials.atom_phong_material import PhongMaterial
from objects.mesh import Mesh
import numpy as np

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
            material = PhongMaterial(properties={"base_color": ELEMENT_COLOR[atom_symbol]})
            material.settings["cull_face"] = True
            material.settings["back_side"] = False
            if   atom_symbol == "H":
                self._atoms_parameters[atom_symbol] = (hydrogen_geometry.HydrogenGeometry(), material)
            elif atom_symbol == "C":
                self._atoms_parameters[atom_symbol] = (carbon_geometry.CarbonGeometry(), material)
            elif atom_symbol == "N":
                self._atoms_parameters[atom_symbol] = (nitrogen_geometry.NitrogenGeometry(), material)
            elif atom_symbol == "O":
                self._atoms_parameters[atom_symbol] = (oxygen_geometry.OxygenGeometry(), material)
            elif atom_symbol == "I":
                self._atoms_parameters[atom_symbol] = (iodine_geometry.IodineGeometry(), material)

        atom_3d = Atom3D(*self._atoms_parameters[atom_symbol])
        return atom_3d






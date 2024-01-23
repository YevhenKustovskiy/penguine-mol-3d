from general.globals import ELEMENT_COLOR
from geometries.bonds.single_bond_geometry import SingleBondGeometry
from geometries.bonds.double_bond_geometry import DoubleBondGeometry
from geometries.bonds.triple_bond_geometry import TripleBondGeometry
from geometries.base_geometry_group import BaseGeometryGroup
from materials.bond_phong_material import PhongMaterial
from objects.mesh import Mesh
from operations.vector_operations import VectorOperations
from operations.matrix_operations import MatrixOperations
from objects.base_object_3d import BaseObject3D
from rdkit.Chem.rdchem import BondType
import numpy as np
import time
from general.attribute import Attribute


def translate_vector(path: np.ndarray, normal: np.ndarray, value):
    """Translates points of a bond path in a direction (axis)
       orthogonal to path direction and normal of three atom's plane
       NOTE: this transformation is nesessary to generate double and triple bonds
    """
    curr_dir = path[0] - path[1]
    curr_dir /= np.linalg.norm(curr_dir)
    axis = np.cross(curr_dir, normal)
    axis /= np.linalg.norm(axis)

    path += (value * axis)

class Bonds3D(Mesh):
    def __init__(self, geometry, material):
        Mesh.__init__(self, geometry, material)


class BondsGeometry(BaseGeometryGroup):
    def __init__(self):
        BaseGeometryGroup.__init__(self)

    def add_bond(self, bond):
        BaseGeometryGroup.add_geometry(self, bond)

class SingleBond(SingleBondGeometry):
    def __init__(self,
                 path_points: list[list[float]],
                 path_colors: list[list[float]],
                 material,
                 normal: np.ndarray = None):

        SingleBondGeometry.__init__(self,
                                    np.array(path_points),
                                    np.array(path_colors))



class DoubleBond(DoubleBondGeometry):
    def __init__(self,
                 path_points: list[list[float]],
                 path_colors: list[list[float]],
                 material,
                 normal: np.ndarray = None):

        f_bond_path = np.array(path_points)
        translate_vector(f_bond_path, normal, 0.1)

        DoubleBondGeometry.__init__(self, f_bond_path, np.array(path_colors))

        s_bond_path = np.array(path_points)
        translate_vector(s_bond_path, normal, -0.1)

        s_bond_geo = DoubleBondGeometry(s_bond_path,
                                        np.array(path_colors))

        self.merge(s_bond_geo)

class TripleBond(TripleBondGeometry):
    """Triple bond mesh"""
    def __init__(self,
                 path_points: list[list[float]],
                 path_colors: list[list[float]],
                 material,
                 normal: np.ndarray = None):

        f_bond_path = np.array(path_points)
        translate_vector(f_bond_path, normal, -0.2)

        TripleBondGeometry.__init__(self, f_bond_path, np.array(path_colors))


        s_bond_path = np.array(path_points)
        s_bond_geo = TripleBondGeometry(s_bond_path,
                                        np.array(path_colors))

        t_bond_path = np.array(path_points)
        translate_vector(t_bond_path, normal, 0.2)
        t_bond_geo = TripleBondGeometry(t_bond_path,
                                        np.array(path_colors))

        self.merge(s_bond_geo)
        self.merge(t_bond_geo)


class BondsFactory:
    """Generates 3D models of bonds"""
    def __init__(self):
        self._bonds = BondsGeometry()
        self._material = PhongMaterial(properties={"use_vertex_colors" : True})
        self._material.settings["cull_face"] = True
        self._material.settings["front_side"] = False
        self._bond_types = {BondType.SINGLE : SingleBond,
                            BondType.DOUBLE : DoubleBond,
                            BondType.TRIPLE : TripleBond}

    def create_bond_geometry(self,
                             path_points: list[list[float]],
                             bond_type: BondType,
                             beg_atom_symbol: str,
                             end_atom_symbol: str,
                             normal: np.ndarray = None
                             ):
        """Generates and returns a 3D model of bond with specified geometry (type) and material"""
        beg_atom_color = ELEMENT_COLOR[beg_atom_symbol]
        end_atom_color = ELEMENT_COLOR[end_atom_symbol]

        curr_dir = np.array(path_points[0]) - np.array(path_points[1])
        curr_dir /= np.linalg.norm(curr_dir)

        midpoint = np.array(VectorOperations.calc_midpoint(path_points[0],
                                                  path_points[1]))

        midpoint1 = midpoint.copy()
        midpoint1 -= (0.0001 * curr_dir)
        midpoint2 = midpoint.copy()
        midpoint2 += (0.0001 * curr_dir)


        bond3d = self._bond_types[bond_type]([path_points[0], midpoint1, midpoint2, path_points[1]],
                                             [beg_atom_color, beg_atom_color, end_atom_color, end_atom_color],
                                             self._material,
                                             normal=normal)


        self._bonds.add_bond(bond3d)

    def get_bonds(self) -> Bonds3D:
        self._bonds.create_attributes()

        for attribute in self._bonds.attributes.values():
            attribute.upload_data()

        return Bonds3D(self._bonds, self._material)









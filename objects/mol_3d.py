from rdkit.Chem.rdchem import BondType, Mol, Atom

from PenguinMol3D.factories.atoms_factory import AtomsFactory, Atom3D
from PenguinMol3D.factories.bonds_factory import BondsFactory, Bonds3D
from PenguinMol3D.general.bounding_box import BoundingBox
from PenguinMol3D.objects.base_object_3d import BaseObject3D
from PenguinMol3D.operations.matrix_operations import MatrixOperations
from PenguinMol3D.operations.plane_operations import ParametricPlane


class Mol3D(BaseObject3D):
    def __init__(self, mol: Mol):
        BaseObject3D.__init__(self)

        self._mol_rdkit = mol
        self._current_conformer = 0
        self._3d_atoms = {}
        self._3d_bonds = []
        self._bounding_box = None
        self._calc_bounding_box()

        self._generate_3d_model()

    @property
    def atoms(self) -> dict[Atom3D]:
        return self._3d_atoms

    @property
    def bonds(self) -> list[Bonds3D]:
        return self._3d_bonds

    @property
    def bounding_box(self) -> BoundingBox:
        return self._bounding_box

    def _add_bonds(self, bond: Bonds3D):
        self._3d_bonds = bond
        self.add_child(bond)

    def _calc_bounding_box(self):
        """Calculates bounding box of a model"""
        conformer = self._mol_rdkit.GetConformer(self._current_conformer)
        x, y, z = [], [], []
        for position in conformer.GetPositions():
            x.append(position[0])
            y.append(position[1])
            z.append(position[2])

        self._bounding_box = BoundingBox(min(x), max(x), min(y), max(y), min(z), max(z))

    def _translate_to_origin(self, position):

        position[0] -= self._bounding_box.x_center_factor
        position[1] -= self._bounding_box.y_center_factor
        position[2] -= self._bounding_box.z_center_factor


    def _add_atom_transform(self, factory: AtomsFactory, atom_symbol: str, atom_position: list[float]):
        transform = MatrixOperations.make_identity()
        transform.itemset((0, 3), atom_position[0])
        transform.itemset((1, 3), atom_position[1])
        transform.itemset((2, 3), atom_position[2])

        if not atom_symbol in self._3d_atoms:
            self._3d_atoms[atom_symbol] = factory.get_atom_3d(atom_symbol)
            self.add_child(self._3d_atoms[atom_symbol])

        self._3d_atoms[atom_symbol].add_instance(transform)

    def _generate_3d_model(self):
        """Generates 3D model based on molecular data"""

        conformer = self._mol_rdkit.GetConformer(self._current_conformer)
        atoms_factory = AtomsFactory()
        bonds_factory = BondsFactory()

        processed_atoms = []
        for bond in self._mol_rdkit.GetBonds():
            first_atom_idx = bond.GetBeginAtomIdx()
            second_atom_idx = bond.GetEndAtomIdx()

            first_atom = self._mol_rdkit.GetAtomWithIdx(first_atom_idx)
            second_atom = self._mol_rdkit.GetAtomWithIdx(second_atom_idx)

            first_atom_symbol = first_atom.GetSymbol()
            second_atom_symbol = second_atom.GetSymbol()

            first_atom_position = list(conformer.GetAtomPosition(first_atom_idx))
            second_atom_position = list(conformer.GetAtomPosition(second_atom_idx))

            self._translate_to_origin(first_atom_position)
            self._translate_to_origin(second_atom_position)

            if not first_atom_idx in processed_atoms:
                self._add_atom_transform(atoms_factory, first_atom_symbol, first_atom_position)
                processed_atoms.append(first_atom_idx)

            if not second_atom_idx in processed_atoms:
                self._add_atom_transform(atoms_factory, second_atom_symbol, second_atom_position)
                processed_atoms.append(second_atom_idx)

            bond_type = bond.GetBondType()
            normal = None
            if bond_type > BondType.SINGLE:
                third_atom_idx = self._find_third_atom(first_atom, second_atom)
                third_atom_symbol = self._mol_rdkit.GetAtomWithIdx(third_atom_idx).GetSymbol()
                third_atom_position = list(conformer.GetAtomPosition(third_atom_idx))

                self._translate_to_origin(third_atom_position)

                if not third_atom_idx in processed_atoms:
                    self._add_atom_transform(atoms_factory, third_atom_symbol, third_atom_position)
                    processed_atoms.append(third_atom_idx)

                three_atoms_plane = ParametricPlane.from_three_points(first_atom_position,
                                                                      second_atom_position,
                                                                      third_atom_position)
                three_atoms_plane.normalize()
                normal = three_atoms_plane.normal

            bonds_factory.create_bond_geometry([first_atom_position, second_atom_position],
                                                bond_type,
                                                first_atom_symbol,
                                                second_atom_symbol,
                                                normal=normal)


        self._add_bonds(bonds_factory.get_bonds())


    def _find_third_atom(self, atom1: Atom, atom2: Atom) -> int:
        """Finds any other third atom connected to atom1 or atom2 and returns its index"""

        third_atom_bonds = list(atom1.GetBonds())
        this_atom_idx = atom1.GetIdx()
        check_atom_idx = atom2.GetIdx()

        if len(third_atom_bonds) == 1:
            third_atom_bonds = list(atom2.GetBonds())
            this_atom_idx = atom2.GetIdx()
            check_atom_idx = atom1.GetIdx()

        for t_bond in third_atom_bonds:
            other_atom_idx = t_bond.GetOtherAtomIdx(this_atom_idx)
            if other_atom_idx != check_atom_idx:
                return other_atom_idx




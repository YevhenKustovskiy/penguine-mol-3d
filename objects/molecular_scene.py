from PenguinMol3D.objects.mol_3d import Mol3D
from PenguinMol3D.objects.scene import Scene


class MolecularScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self._molecules = []

    def add_molecule(self, mol: Mol3D):
        self._molecules.append(mol)
        self.add_child(mol)

    def get_molecules(self) -> list[Mol3D]:
        return self._molecules

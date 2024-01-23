from geometries.atoms.base_atom_geometry import BaseAtomGeometry


class SulfurGeometry(BaseAtomGeometry):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SulfurGeometry, cls).__new__(cls)
        return cls.instance


    def __init__(self):
        BaseAtomGeometry.__init__(self, radius= 0.41)
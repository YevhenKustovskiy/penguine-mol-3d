from geometries.atoms.base_atom_geometry import BaseAtomGeometry


class HydrogenGeometry(BaseAtomGeometry):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(HydrogenGeometry, cls).__new__(cls)
        return cls.instance

    def __init__(self):

        BaseAtomGeometry.__init__(self, radius=0.28)
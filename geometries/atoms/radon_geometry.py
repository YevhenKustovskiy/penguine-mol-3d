from geometries.atoms.base_atom_geometry import BaseAtomGeometry


class RadonGeometry(BaseAtomGeometry):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(RadonGeometry, cls).__new__(cls)
        return cls.instance


    def __init__(self):
        BaseAtomGeometry.__init__(self, radius = 0.50)
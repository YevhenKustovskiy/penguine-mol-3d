from OpenGL.GL import *
from objects.base_object_3d import BaseObject3D
from geometries.base_geometry import BaseGeometry
from materials.base_material import BaseMaterial


class Mesh(BaseObject3D):
    def __init__(self, geometry: BaseGeometry, material: BaseMaterial):
        BaseObject3D.__init__(self)
        self._geometry = geometry
        self._material = material
        self._visible = True

        self._vao_ref = glGenVertexArrays(1)
        glBindVertexArray(self._vao_ref)
        for variable_name, attribute_object in \
            self._geometry.attributes.items():
            attribute_object.associate_variable(material.program_ref,
                                                variable_name)
        glBindVertexArray(0)

    @property
    def geometry(self) -> BaseGeometry:
        return self._geometry

    @property
    def material(self) -> BaseMaterial:
        return self._material

    @property
    def vao_ref(self):
        return self._vao_ref

    @property
    def visible(self) -> bool:
        return self._visible



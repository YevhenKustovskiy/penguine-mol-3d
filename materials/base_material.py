from OpenGL.GL import *

from PenguinMol3D.general.opengl_utils import OpenGLUtils
from PenguinMol3D.general.uniform import Uniform


class BaseMaterial:
    """Base material class"""
    def __init__(self, vert_shader_path: str, frag_shader_path: str):

        self._program_ref = OpenGLUtils.initialize_program(vert_shader_path,
                                                           frag_shader_path)
        """Transform related uniforms"""
        self._uniforms = {}
        self._uniforms["view_matrix"]       = Uniform(None, "mat4")
        self._uniforms["projection_matrix"] = Uniform(None, "mat4")

        """Material related uniforms"""
        self._uniforms["specular_strength"] = Uniform(None, "float")
        self._uniforms["shininess"]         = Uniform(None, "float")

        """Lighting related uniforms"""
        self._uniforms["light0"]            = Uniform(None, "Light")
        self._uniforms["light1"]            = Uniform(None, "Light")
        self._uniforms["light2"]            = Uniform(None, "Light")
        self._uniforms["light3"]            = Uniform(None, "Light")

        self._settings = {}
        self._settings["use_instanced_rendering"] = False
        self._settings["draw_style"] = GL_TRIANGLES

    @property
    def program_ref(self):
        return self._program_ref

    @property
    def uniforms(self) -> dict:
        return self._uniforms

    @property
    def settings(self) -> dict:
        return self._settings

    def add_uniform(self, data: int|float|list, dtype: str, name: str):
        self._uniforms[name] = Uniform(data, dtype)

    def locate_uniform(self, name: str):
        self._uniforms[name].locate_variable(self._program_ref, name)

    def locate_uniforms(self):
        for name, object in self._uniforms.items():
            object.locate_variable(self._program_ref, name)

    def update_render_settings(self):
        pass

    def set_properties(self, properties: dict):
        for name, data in properties.items():
            if name in self._uniforms:
                self._uniforms[name].data = data
            elif name in self._settings:
                self._settings[name] = data
            else:
                raise Exception("Material has no property named:" + name)





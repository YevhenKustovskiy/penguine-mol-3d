import os
from OpenGL.GL import *
from PenguinMol3D.materials.base_material import BaseMaterial

"""
   This module contains class, which uses a modern physically based lighting model. 
   You can create your own materials by subclassing it and configuring 
   'metallic', 'roughness', and 'ao' uniform values to get unique visual appearance

   NOTE: a sum of 'metallic' and 'roughness' should not exceed 1.0
"""

class PBRMaterial(BaseMaterial):
    def __init__(self, properties={}):

        vert_shader_name = "base.vert"
        if properties["use_instanced_rendering"]:
            vert_shader_name = "instanced.vert"

        vert_shader_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "shaders",
                                        vert_shader_name)

        frag_shader_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "shaders",
                                        "pbr_material.frag")

        BaseMaterial.__init__(self, vert_shader_path, frag_shader_path)

        if not properties["use_instanced_rendering"]:
            self.add_uniform(None, "mat4", "model_matrix")

        self.add_uniform(False, "bool", "use_vertex_colors")
        self.add_uniform([1., 1., 1.], "vec3", "base_color")
        self.add_uniform([0., 0., 0.], "vec3", "view_position")

        # Physics based rendering uniforms
        self.add_uniform(0.5, "float", "metallic")
        self.add_uniform(0.5, "float", "roughness")
        self.add_uniform(1.0, "float", "ao")

        self.locate_uniforms()

        self._settings["cull_face"] = False
        self._settings["front_side"] = True
        self._settings["back_side"] = True
        self._settings["wireframe"] = False
        self._settings["line_width"] = 1

        self.set_properties(properties)
        self.update_render_settings()

    def update_render_settings(self):

        if not self._settings["cull_face"]:
            glDisable(GL_CULL_FACE)
        else:
            glEnable(GL_CULL_FACE)

        if not self._settings["front_side"]:
            glCullFace(GL_FRONT)

        if not self._settings["back_side"]:
            glCullFace(GL_BACK)

        if self._settings["wireframe"]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glLineWidth(self._settings["line_width"])
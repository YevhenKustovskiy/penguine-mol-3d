"""PenguinMol3D: 3D visualization of small compounds
   Copyright (C) 2024  Yevhen Kustovskiy

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License along
   with this program; if not, write to the Free Software Foundation, Inc.,
   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA. """

import os
import glfw
import glfw.GLFW as GLFW_CONSTANTS
from OpenGL.GLUT import *
from rdkit.Chem import MolFromMolFile, Kekulize

#from PenguinMol3D.general.renderer import Renderer
#from PenguinMol3D.objects.camera import Camera
#from PenguinMol3D.objects.light.ambient import Ambient
#from PenguinMol3D.objects.light.directional import Directional
#from PenguinMol3D.objects.light.point import Point
#from PenguinMol3D.objects.mol_3d import Mol3D
#from PenguinMol3D.objects.molecular_scene import MolecularScene
#from PenguinMol3D.objects.trackball import Trackball
from PenguinMol3D.general.renderer import Renderer
from PenguinMol3D.objects.camera import Camera
from PenguinMol3D.objects.light.directional import Directional
from PenguinMol3D.objects.mol_3d import Mol3D
from PenguinMol3D.objects.molecular_scene import MolecularScene
from PenguinMol3D.objects.trackball import Trackball
from PenguinMol3D.materials import (
    phong_material,
    pbr_material
)

"""Rendering rough surface using Blinn-Phong Lighting Model"""
class CustomPhongMaterial(phong_material.PhongMaterial):
    def __init__(self, properties: dict = {}):
        phong_material.PhongMaterial.__init__(self, properties=properties)
        self.uniforms["shininess"].data = 15.0

"""Rendering rough surface using Physically Based Lighting Model"""
class CustomPBRMaterial(pbr_material.PBRMaterial):
    def __init__(self, properties: dict = {}):
        pbr_material.PBRMaterial.__init__(self, properties=properties)
        """Sum of metallic and roughness should not exceed 1.0"""
        self.uniforms["metallic"].data = 0.4
        self.uniforms["roughness"].data = 0.6
        self.uniforms["ao"].data = 1.0

class GLFWScreenshotExample:
    def __init__(self, material: phong_material.PhongMaterial | pbr_material.PBRMaterial):
        self.title = "PenguinMol3D - Custom material example"
        self.width = 1000
        self.height = 800
        self.window = None
        self.running = True
        self.prev_pos = None

        self.make_glfw_window()
        self.make_scene(material)

    def make_glfw_window(self):
        """Create window and grab OpenGL context"""
        glfw.init()
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CLIENT_API, GLFW_CONSTANTS.GLFW_OPENGL_API)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_RESIZABLE, GLFW_CONSTANTS.GLFW_FALSE)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_SAMPLES, 8)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_DEPTH_BITS, 24)

        self.window = glfw.create_window(self.width, self.height, self.title, None, None)

        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_cursor_pos_callback(self.window, self.mouse_cursor_callback)
        glfw.set_window_close_callback(self.window, self.close_callback)

        glfw.make_context_current(self.window)

    """GLFW specific methods to handle events"""
    def close_callback(self, window):
        self.running = False

    def mouse_cursor_callback(self, window, xpos: float, ypos: float):
        left_mouse_button = glfw.get_mouse_button(window, GLFW_CONSTANTS.GLFW_MOUSE_BUTTON_LEFT)
        if left_mouse_button == GLFW_CONSTANTS.GLFW_PRESS:
            if self.prev_pos:
                """Use trackball to convert previous and current cursor coordinates into rotational matrix"""
                rotmat = Trackball.simulate_trackball([self.width, self.height],
                                                      [xpos, ypos],
                                                      [self.prev_pos[0], self.prev_pos[1]])
                self.mol_3d.apply_transform(rotmat, local_coord=False)
            self.prev_pos = (xpos, ypos)

        right_mouse_button = glfw.get_mouse_button(window, GLFW_CONSTANTS.GLFW_MOUSE_BUTTON_RIGHT)
        if right_mouse_button == GLFW_CONSTANTS.GLFW_PRESS:
            if self.prev_pos:
                """Scale object to get effect similar to zoom in/zoom out"""
                if self.prev_pos[1] < ypos:
                    self.mol_3d.scale(1.1, local_coord=True)
                else:
                    self.mol_3d.scale(0.9, local_coord=True)
            self.prev_pos = (xpos, ypos)

        if left_mouse_button == GLFW_CONSTANTS.GLFW_RELEASE and \
                right_mouse_button == GLFW_CONSTANTS.GLFW_RELEASE:
            self.prev_pos = None

    def key_callback(self, window, key: int, scancode: int, action: int, mods):
        if key == GLFW_CONSTANTS.GLFW_KEY_ESCAPE and action == GLFW_CONSTANTS.GLFW_PRESS:
            self.running = False

        if key == GLFW_CONSTANTS.GLFW_KEY_S and action == GLFW_CONSTANTS.GLFW_PRESS:
            self.renderer.save_frame(self.width, self.height, "penguinone.png")

    def make_scene(self, material: phong_material.PhongMaterial | pbr_material.PBRMaterial):
        """Create the Renderer object and setup the Scene"""
        self.renderer = Renderer(clear_color=[1., 1., 1.])
        self.scene = MolecularScene()
        self.camera = Camera(angle_of_view=60,
                             aspect_ratio=self.width / self.height,
                             far=1000)

        """Load molecular data from file using one of the RDKit functions"""
        mol_rdkit = MolFromMolFile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "penguinone.sdf"),
                                   sanitize=True,
                                   removeHs=False)

        Kekulize(mol_rdkit, clearAromaticFlags=True)

        """Pass rdkit Mol object and custom material to Mol3D constructor"""
        self.mol_3d = Mol3D(mol_rdkit,
                            material_type=material,
                            color_scale=1.0)
        self.scene.add_molecule(self.mol_3d)
        self.camera.set_bb_based_position(self.mol_3d.bounding_box)

        dl0, dl1, dl2 = None, None, None
        if material == CustomPhongMaterial:
            dl0 = Directional(color=[3.0, 3.0, 3.0])
            dl1 = Directional(color=[1.5, 1.5, 1.5])
            dl2 = Directional(color=[3.0, 3.0, 3.0])
        else:
            dl0 = Directional(color=[300.0, 300.0, 300.0])
            dl1 = Directional(color=[150.0, 150.0, 150.0])
            dl2 = Directional(color=[300.0, 300.0, 300.0])

        dl0.set_position([8.,8.,8])
        dl0.look_at(self.scene.get_position())
        self.scene.add_child(dl0)

        dl1.set_position(self.camera.get_position())
        dl1.look_at(self.scene.get_position())
        self.scene.add_child(dl1)

        dl2.set_position([0., 8., 0.])
        dl2.look_at(self.scene.get_position())
        self.scene.add_child(dl2)

    def run_application(self):
        """Run application event loop until user decides to quit"""
        while self.running:
            self.renderer.render(self.scene, self.camera)
            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.destroy_window(self.window)
        glfw.terminate()

if __name__ == "__main__":
    #app = GLFWScreenshotExample(CustomPhongMaterial)
    app = GLFWScreenshotExample(CustomPBRMaterial)
    app.run_application()


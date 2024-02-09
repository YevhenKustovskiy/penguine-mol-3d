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

from PenguinMol3D.general.renderer import Renderer
from PenguinMol3D.objects.camera import Camera
from PenguinMol3D.objects.light.directional import Directional
from PenguinMol3D.objects.mol_3d import Mol3D
from PenguinMol3D.objects.molecular_scene import MolecularScene
from PenguinMol3D.materials.pbr_material import PBRMaterial

class GLFWSurfaceExample:
    def __init__(self):
        self.title = "PenguinMol3D - GLFW surface example"
        self.width = 1000
        self.height = 800
        self.window = None
        self.running = True

        self.make_glfw_window()
        self.make_scene()

    def make_glfw_window(self):
        """Create window and grab OpenGL context"""
        glfw.init()
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CLIENT_API, GLFW_CONSTANTS.GLFW_OPENGL_API)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_RESIZABLE, GLFW_CONSTANTS.GLFW_FALSE)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_SAMPLES, 4)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_DEPTH_BITS, 16)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_RED_BITS, 16)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_GREEN_BITS, 16)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_BLUE_BITS, 16)

        self.window = glfw.create_window(self.width, self.height, self.title, None, None)

        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_window_close_callback(self.window, self.close_callback)

        glfw.make_context_current(self.window)

    """GLFW specific methods to handle events"""
    def close_callback(self, window):
        self.running = False

    def key_callback(self, window, key, scancode, action, mods):
        if key == GLFW_CONSTANTS.GLFW_KEY_ESCAPE and action == GLFW_CONSTANTS.GLFW_PRESS:
            self.running = False

    def make_scene(self):
        """Create the Renderer object and setup the Scene"""
        self.renderer = Renderer(clear_color=[1., 1., 1.])
        self.scene = MolecularScene()
        self.camera = Camera(angle_of_view=60,
                             aspect_ratio=self.width / self.height,
                             far=100)

        """Load molecular data from file using one of the RDKit functions"""
        mol_rdkit = MolFromMolFile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "penguinone.sdf"),
                                   sanitize=True,
                                   removeHs=False)
        Kekulize(mol_rdkit, clearAromaticFlags=True)

        """Pass rdkit Mol object as an argument to Mol3D constructor"""
        self.mol_3d = Mol3D(mol_rdkit,
                            material_type=PBRMaterial)
        self.scene.add_molecule(self.mol_3d)
        self.camera.set_bb_based_position(self.mol_3d.bounding_box)
        self.mol_3d.bounding_box.center

        dl0 = Directional(color=[300.0, 300.0, 300.0])
        dl0.set_position([8., 8., 8])
        dl0.look_at(self.scene.get_position())
        self.scene.add_child(dl0)

        dl1 = Directional(color=[150.0, 150.0, 150.0])
        dl1.set_position(self.camera.get_position())
        dl1.look_at(self.scene.get_position())
        self.scene.add_child(dl1)

        dl2 = Directional(color=[300.0, 300.0, 300.0])
        dl2.set_position([0., 8., 0.])
        dl2.look_at(self.scene.get_position())
        self.scene.add_child(dl2)

    def run_application(self):
        """Run application event loop until user decides to quit"""
        while self.running:
            self.mol_3d.rotate_y(0.005)
            self.renderer.render(self.scene, self.camera)
            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.destroy_window(self.window)
        glfw.terminate()

if __name__ == "__main__":
    app = GLFWSurfaceExample()
    app.run_application()


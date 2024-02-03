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

import glfw
import glfw.GLFW as GLFW_CONSTANTS
from OpenGL.GLUT import *
from rdkit.Chem import (
    MolFromMolFile,
    MolFromMol2File,
    Kekulize
)

from PenguinMol3D.general.renderer import Renderer
from PenguinMol3D.objects.camera import Camera
from PenguinMol3D.objects.light.ambient import Ambient
from PenguinMol3D.objects.light.directional import Directional
from PenguinMol3D.objects.light.point import Point
from PenguinMol3D.objects.mol_3d import Mol3D
from PenguinMol3D.objects.molecular_scene import MolecularScene
from PenguinMol3D.objects.trackball import Trackball



def load_molecule(path: str, removeHs: bool = False):
    """Loads molecular data from file using RDKit functions"""

    mol_rdkit = None
    ext = path.split(".")[-1]
    if ext == "sdf" or ext == "mol":
        mol_rdkit = MolFromMolFile(path,
                                   sanitize=True,
                                   removeHs=removeHs)

    elif ext == "mol2":
        mol_rdkit = MolFromMol2File(path,
                                    sanitize=True,
                                    removeHs=removeHs)
    else:
        raise Exception(f"{ext.upper()} format is not currently supported!")

    Kekulize(mol_rdkit, clearAromaticFlags=True)
    return mol_rdkit

class PenguinMol3D:
    def __init__(self):
        self.title = "PenguinMol3D"
        self.width = 1000
        self.height = 800
        self.window = None
        self.running = True
        self.prev_pos = None

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
                rotmat = Trackball.simulate_trackball([self.width, self.height],
                                                      [xpos, ypos],
                                                      [self.prev_pos[0], self.prev_pos[1]])
                self.mol_3d.apply_transform(rotmat, local_coord=False)
            self.prev_pos = (xpos, ypos)

        right_mouse_button = glfw.get_mouse_button(window, GLFW_CONSTANTS.GLFW_MOUSE_BUTTON_RIGHT)
        if right_mouse_button == GLFW_CONSTANTS.GLFW_PRESS:
            if self.prev_pos:
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
            filepath = sys.argv[1].split(".")[0] + ".png"
            self.renderer.save_frame(self.width, self.height, filepath)

    def make_scene(self):
        """Create the Renderer object and setup the Scene"""
        self.renderer = Renderer()
        self.scene = MolecularScene()
        self.camera = Camera(angle_of_view=60,
                             aspect_ratio=self.width / self.height,
                             far=100)

        self.ambient = Ambient(color=[0.1, 0.1, 0.1])
        self.scene.add_child(self.ambient)

        self.directional = Directional(color=[1.0, 1.0, 1.0],
                                       direction=[-1., -1., -2.])

        self.scene.add_child(self.directional)

        self.point = Point(position=[2., 2., 2.])
        self.scene.add_child(self.point)

        """Load rdkit Mol object and pass it as an argument to Mol3D constructor"""
        self.mol_3d = Mol3D(load_molecule(sys.argv[1]),
                            material_type="rubber")
        self.scene.add_molecule(self.mol_3d)
        self.camera.set_bb_based_position(self.mol_3d.bounding_box)

    def run_application(self):
        """Run application event loop until user decides to quit"""
        while self.running:
            self.renderer.render(self.scene, self.camera)
            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.destroy_window(self.window)
        glfw.terminate()

if __name__ == "__main__":
    app = PenguinMol3D()
    app.run_application()


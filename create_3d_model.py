import os
import sys
from OpenGL.GLUT import *
import glfw
import glfw.GLFW as GLFW_CONSTANTS

from rdkit.Chem import (
    MolFromMolFile,
    MolFromMol2File,
    MolFromXYZFile,
    Kekulize
)

from objects.camera import Camera
from objects.light.ambient import Ambient
from objects.light.directional import Directional
from objects.light.point import Point
from objects.molecular_scene import MolecularScene
from objects.mol_3d import Mol3D
from general.renderer import Renderer
from objects.trackball import Trackball


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

class PenguineMol3D:
    def __init__(self):
        self.title = "PenguineMol3D"
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
        self.mol_3d = Mol3D(load_molecule(sys.argv[1]))
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
    app = PenguineMol3D()
    app.run_application()


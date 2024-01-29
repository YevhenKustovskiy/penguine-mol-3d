from OpenGL.GL import *
from PIL.Image import frombytes

from PenguinMol3D.objects.camera import Camera
from PenguinMol3D.objects.light.base_light import BaseLight
from PenguinMol3D.objects.molecular_scene import MolecularScene


class Renderer:
    def __init__(self, clear_color: list[float] = [0., 0. ,0.]):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glClearColor(clear_color[0], clear_color[1], clear_color[2], 1)

    def _render_lights(self, lights, mesh):
        if "light0" in mesh.material.uniforms.keys():
            for light_number in range(4):
                light_name = f"light{str(light_number)}"
                light_object = lights[light_number]
                mesh.material.uniforms[light_name].data = light_object

    def _render_atoms(self, atoms, lights, camera_pos, camera_view, camera_proj):
        for atom in atoms:
            glUseProgram(atom.material.program_ref)
            glBindVertexArray(atom.vao_ref)

            instances = atom.get_instances()
            for no, instance in enumerate(instances):
                atom.material.uniforms[f"model_matrix[{no}]"].data = atom.get_world_transform() @ instance

            atom.material.uniforms["view_matrix"].data = camera_view
            atom.material.uniforms["projection_matrix"].data = camera_proj

            if "view_position" in atom.material.uniforms.keys():
                atom.material.uniforms["view_position"].data = camera_pos

            self._render_lights(lights, atom)

            for uniform in atom.material.uniforms.values():
                uniform.upload_data()

            atom.material.update_render_settings()

            glDrawArraysInstanced(atom.material.settings["draw_style"],
                                  0,
                                  atom.geometry.num_vertices,
                                  len(instances))

            glBindVertexArray(0)

    def _render_bonds(self, bonds, lights, camera_pos, camera_view, camera_proj):
        glUseProgram(bonds.material.program_ref)
        glBindVertexArray(bonds.vao_ref)

        bonds.material.uniforms["model_matrix"].data = bonds.get_world_transform()
        bonds.material.uniforms["view_matrix"].data = camera_view
        bonds.material.uniforms["projection_matrix"].data = camera_proj

        if "view_position" in bonds.material.uniforms.keys():
            bonds.material.uniforms["view_position"].data = camera_pos

        self._render_lights(lights, bonds)

        for uniform in bonds.material.uniforms.values():
            uniform.upload_data()

        bonds.material.update_render_settings()

        glDrawArrays(bonds.material.settings["draw_style"],0,bonds.geometry.num_vertices)
        glBindVertexArray(0)

    def render(self, scene: MolecularScene, camera: Camera):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        camera.update_view()

        descendants = scene.get_descendants()

        light_filter = lambda x: isinstance(x, BaseLight)
        lights = list(filter(light_filter, descendants))

        while len(lights) < 4:
            lights.append(BaseLight())

        camera_pos  = camera.get_world_position()
        camera_view = camera.view
        camera_proj = camera.projection

        molecule = scene.get_molecules()[0]

        self._render_atoms(molecule.atoms.values(), lights, camera_pos, camera_view, camera_proj)
        self._render_bonds(molecule.bonds, lights, camera_pos, camera_view, camera_proj)

    def save_frame(self, width: int, height: int, filepath: str):
        content = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
        image = frombytes("RGB", (width, height), content, "raw", "RGB", 0, 1)
        image = image.transpose(1)
        image.save(filepath)







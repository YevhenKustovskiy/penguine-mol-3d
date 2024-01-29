from OpenGL.GL import *


class Uniform:
    def __init__(self, data: int|float|list, dtype: str):
        self._data = data
        self._dtype = dtype
        self._variable_ref = None

    def __iadd__(self, other):
        self._data += other
        return self

    def __isub__(self, other):
        self._data -= other
        return self

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def locate_variable(self, program_ref, variable_name):
        if self._dtype == "Light":
            self._variable_ref = {}
            self._variable_ref["light_type"] = \
                glGetUniformLocation(program_ref, f"{variable_name}.light_type")
            self._variable_ref["color"] = \
                glGetUniformLocation(program_ref, f"{variable_name}.color")
            self._variable_ref["direction"] = \
                glGetUniformLocation(program_ref, f"{variable_name}.direction")
            self._variable_ref["position"] = \
                glGetUniformLocation(program_ref, f"{variable_name}.position")
            self._variable_ref["attenuation"] = \
                glGetUniformLocation(program_ref, f"{variable_name}.attenuation")
        else:
            self._variable_ref = glGetUniformLocation(program_ref, variable_name)

    def upload_data(self):
        if self._variable_ref == -1:
            return

        if self._dtype == "int":

            glUniform1i(self._variable_ref,
                        self._data)
            return

        if self._dtype == "bool":

            glUniform1i(self._variable_ref,
                        self._data)
            return

        if self._dtype == "float":

            glUniform1f(self._variable_ref,
                        self._data)
            return

        if self._dtype == "vec2":

            glUniform2f(self._variable_ref,
                        self._data[0],
                        self._data[1])
            return

        if self._dtype == "vec3":

            glUniform3f(self._variable_ref,
                        self._data[0],
                        self._data[1],
                        self._data[2])
            return

        if self._dtype == "vec4":

            glUniform4f(self._variable_ref,
                        self._data[0],
                        self._data[1],
                        self._data[2],
                        self._data[3])
            return

        if self._dtype == "mat4":

            glUniformMatrix4fv(self._variable_ref,
                               1,
                               GL_TRUE,
                               self._data)
            return

        if self._dtype == "Light":
            glUniform1i(self._variable_ref["light_type"],
                        self._data.light_type)

            glUniform3f(self._variable_ref["color"],
                        self._data.color[0],
                        self._data.color[1],
                        self._data.color[2])

            direction = self._data.get_direction()
            glUniform3f(self._variable_ref["direction"],
                        direction[0],
                        direction[1],
                        direction[2])

            position = self._data.get_position()
            glUniform3f(self._variable_ref["position"],
                        position[0],
                        position[1],
                        position[2])

            glUniform3f(self._variable_ref["attenuation"],
                        self._data.attenuation[0],
                        self._data.attenuation[1],
                        self._data.attenuation[2])
            return

        raise Exception(f"Variable has unknown type {self._dtype}")

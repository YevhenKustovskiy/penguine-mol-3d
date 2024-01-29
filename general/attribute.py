from ctypes import c_void_p

import numpy as np
from OpenGL.GL import *


class Attribute:
    def __init__(self, data: int|float|list, dtype: str):

        self._data = data
        self._dtype = dtype
        self._buffer_ref = glGenBuffers(1)
        self._n_variable = 0

        self.upload_data()

    @property
    def data(self) -> int|float|list:
        return self._data

    @data.setter
    def data(self, data: int | float | list):
        self._data = data

    def associate_variable(self, program_ref, variable_name):
        variable_ref = glGetAttribLocation(program_ref, variable_name)

        if variable_ref == -1:
            return

        glBindBuffer(GL_ARRAY_BUFFER, self._buffer_ref)

        if self._dtype == "int":
            glEnableVertexAttribArray(variable_ref)
            glVertexAttribPointer(variable_ref,1,GL_INT,False,0,None)
        elif self._dtype == "float":
            glEnableVertexAttribArray(variable_ref)
            glVertexAttribPointer(variable_ref,1,GL_FLOAT,False,0,None)
        elif self._dtype == "vec2":
            glEnableVertexAttribArray(variable_ref)
            glVertexAttribPointer(variable_ref,2,GL_FLOAT,False, 0, None)
        elif self._dtype == "vec3":
            glEnableVertexAttribArray(variable_ref)
            glVertexAttribPointer(variable_ref,3,GL_FLOAT,False, 0, None)
        elif self._dtype == "vec4":
            glEnableVertexAttribArray(variable_ref)
            glVertexAttribPointer(variable_ref,4,GL_FLOAT,False, 0, None)
        elif self._dtype == "mat4":
            glEnableVertexAttribArray(variable_ref)
            glEnableVertexAttribArray(variable_ref + 1)
            glEnableVertexAttribArray(variable_ref + 2)
            glEnableVertexAttribArray(variable_ref + 3)

            glVertexAttribPointer(variable_ref, 4, GL_FLOAT, GL_FALSE, 64, c_void_p(0))

            glVertexAttribPointer(variable_ref + 1, 4, GL_FLOAT, GL_FALSE, 64, c_void_p(16))

            glVertexAttribPointer(variable_ref + 2, 4, GL_FLOAT, GL_FALSE, 64, c_void_p(32))

            glVertexAttribPointer(variable_ref + 3, 4, GL_FLOAT, GL_FALSE, 64, c_void_p(48))

            glVertexAttribDivisor(variable_ref, 1)
            glVertexAttribDivisor(variable_ref + 1, 1)
            glVertexAttribDivisor(variable_ref + 2, 1)
            glVertexAttribDivisor(variable_ref + 3, 1)
        else:
            raise Exception(f"Attribute {variable_name} has unknown type {self._dtype}")

    def upload_data(self):
        data = np.array(self._data, dtype=np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self._buffer_ref)
        if self._dtype == "mat4":
            glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        else:
            glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)

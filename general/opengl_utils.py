from OpenGL.GL import *


class OpenGLUtils:
    @staticmethod
    def initialize_shader(shader_code: str, shader_type: str):
        shader_code = f"#version 330 core\n{shader_code}"
        shader_ref = glCreateShader(shader_type)
        glShaderSource(shader_ref, shader_code)
        glCompileShader(shader_ref)

        compile_success = glGetShaderiv(shader_ref, GL_COMPILE_STATUS)
        if not compile_success:
            error_message = glGetShaderInfoLog(shader_ref).decode("utf-8")
            glDeleteShader(shader_ref)
            raise Exception(f"\n{error_message}")

        return shader_ref

    @staticmethod
    def initialize_program(vert_shader_code: str,
                           frag_shader_code: str
                           ):
        vert_shader_ref = OpenGLUtils.initialize_shader(vert_shader_code,
                                                          GL_VERTEX_SHADER)
        frag_shader_ref = OpenGLUtils.initialize_shader(frag_shader_code,
                                                          GL_FRAGMENT_SHADER)
        program_ref = glCreateProgram()

        glAttachShader(program_ref, vert_shader_ref)
        glAttachShader(program_ref, frag_shader_ref)
        glLinkProgram(program_ref)

        link_success = glGetProgramiv(program_ref, GL_LINK_STATUS)
        if not link_success:
            error_message = glGetProgramInfoLog(program_ref).decode("utf-8")
            glDeleteProgram(program_ref)
            raise Exception(f"\n{error_message}")

        return program_ref

    @staticmethod
    def print_system_info():
        print("Vendor: " + glGetString(GL_VENDOR).decode("utf-8"))
        print("Renderer: " + glGetString(GL_RENDERER).decode("utf-8"))
        print("OpenGl version supported: " + glGetString(GL_VERSION).decode("utf-8"))
        print("GLSL version supported: " + glGetString(GL_SHADING_LANGUAGE_VERSION).decode("utf-8"))


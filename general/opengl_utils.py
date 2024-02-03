from OpenGL.GL import *


class OpenGLUtils:
    SHADER_TYPE = {"vert" : GL_VERTEX_SHADER,
                   "frag" : GL_FRAGMENT_SHADER}
    @staticmethod
    def load_shader(shader_path: str) -> tuple[str, GL_SHADER_TYPE]:
        shader_file = open(shader_path, "r")
        shader_code = shader_file.read()
        ext = shader_path.split(".")[-1]
        shader_file.close()
        return (shader_code, OpenGLUtils.SHADER_TYPE[ext])

    @staticmethod
    def initialize_shader(shader_path: str) -> int:
        shader_code, shader_type = OpenGLUtils.load_shader(shader_path)
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
    def initialize_program(vert_shader_path: str,
                           frag_shader_path: str
                           ) -> int:
        vert_shader_ref = OpenGLUtils.initialize_shader(vert_shader_path)
        frag_shader_ref = OpenGLUtils.initialize_shader(frag_shader_path)
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


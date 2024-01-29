from OpenGL.GL import *

from PenguinMol3D.materials.base_material import BaseMaterial

class PhongMaterial(BaseMaterial):
    def __init__(self, texture=None, properties={}):
        vert_shader_code = """
                           uniform mat4 projection_matrix;
                           uniform mat4 view_matrix;
                           uniform mat4 model_matrix[100];
                           uniform vec3 base_color;
                           uniform bool use_vertex_colors;
                           
                           in vec3 vertex_position;
                           in vec3 vertex_normal;
                           in vec3 vertex_color;
                           out vec3 position;
                           out vec3 normal;
                           out vec3 color;

                              
                           void main()
                           {
                               mat4 transform = model_matrix[gl_InstanceID];
                               gl_Position = projection_matrix * 
                                             view_matrix * 
                                             transform *
                                             vec4(vertex_position, 1);
                               position = vec3(transform * vec4(vertex_position, 1));
                               normal = normalize(mat3(transform) * vertex_normal);
                               if (use_vertex_colors)
                               {
                                   color = vertex_color;
                               }
                               else
                               {
                                   color = base_color;
                               }
                           }
                           """

        frag_shader_code = """
                           struct Light
                           {
                               int light_type;
                               vec3 color;
                               vec3 direction;
                               vec3 position;
                               vec3 attenuation;
                           };
                           
                           uniform Light light0;
                           uniform Light light1;
                           uniform Light light2;
                           uniform Light light3;
                           uniform vec3 view_position;
                           uniform float specular_strength;
                           uniform float shininess;
                           
                           vec3 light_calc(Light light, vec3 point_position, vec3 point_normal)
                           {
                               float ambient     = 0.0;
                               float diffuse     = 0.0;
                               float specular    = 0.0;
                               float attenuation = 1.0;
                               vec3 light_direction = vec3(0.0, 0.0, 0.0);
                               
                               if (light.light_type == 1)
                               {
                                   ambient = 1;
                               }
                               else if (light.light_type == 2)
                               {
                                   light_direction = normalize(light.direction);
                               }
                               else if (light.light_type == 3)
                               {
                                   light_direction = normalize(point_position - light.position);
                                   float distance = length(light.position - point_position);
                                   attenuation = 1.0 / (light.attenuation[0] + 
                                                        light.attenuation[1] * distance +
                                                        light.attenuation[2] * distance * distance);
                               }
                               
                               if (light.light_type > 1)
                               {
                                   point_normal = normalize(point_normal);
                                   diffuse = max(dot(point_normal, - light.direction), 0.0);
                                   diffuse *= attenuation;
                                   if (diffuse > 0)
                                   {
                                       vec3 view_direction = normalize(view_position-point_position);
                                       vec3 reflect_direction = reflect( light_direction, point_normal);
                                       specular = max(dot(view_direction, reflect_direction), 0.0);
                                       specular = specular_strength * pow(specular, shininess);
                                   }
                               }
                               return light.color * (ambient + diffuse + specular);
                           }
                           in vec3 color;
                           in vec3 position;
                           in vec3 normal;
                           out vec4 frag_color;
                           void main()
                           {
                               vec4 final_color = vec4(color, 1.0);
                               vec3 total = vec3(0., 0., 0.);
                               total += light_calc(light0, position, normal);
                               total += light_calc(light1, position, normal);
                               total += light_calc(light2, position, normal);
                               total += light_calc(light3, position, normal);
                               final_color *= vec4(total, 1.0);
                               frag_color = final_color;
                           }
                           """

        BaseMaterial.__init__(self, vert_shader_code, frag_shader_code)

        self.add_uniform([1., 1., 1.], "vec3", "base_color")
        self.add_uniform(None, "Light", "light0")
        self.add_uniform(None, "Light", "light1")
        self.add_uniform(None, "Light", "light2")
        self.add_uniform(None, "Light", "light3")


        self.add_uniform([0., 0., 0.], "vec3", "view_position")
        self.add_uniform(1.0, "float", "specular_strength")
        self.add_uniform(32.0, "float", "shininess")

        self.locate_uniforms()

        self._settings["cull_face"] = False
        self._settings["front_side"] = True
        self._settings["back_side"] = True
        self._settings["wireframe"]   = False
        self._settings["line_width"]  = 1

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

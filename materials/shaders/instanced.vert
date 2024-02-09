#version 330

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
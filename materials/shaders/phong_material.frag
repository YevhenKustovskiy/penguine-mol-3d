#version 330

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
        diffuse = max(dot(point_normal, -light.direction), 0.0);
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
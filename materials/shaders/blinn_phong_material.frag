#version 330

struct Light
{
    int light_type;
    vec3 color;
    vec3 direction;
    vec3 position;
    vec3 attenuation;
};

uniform Light lights[10];
uniform vec3 view_position;
uniform float specular_strength;
uniform float shininess;

uniform bool use_tone_mapping;
uniform bool use_gamma_correction;


vec3 light_calc(Light light, vec3 point_position, vec3 point_normal)
{
    float diffuse     = 0.0;
    float specular    = 0.0;
    float attenuation = 1.0;
    vec3 light_direction = vec3(0.0, 0.0, 0.0);
    float distance = length(light.position - point_position);

    if (light.light_type == 2)
    {
        light_direction = -normalize(light.direction);
        if (use_gamma_correction)
        {
            attenuation = attenuation / distance;
        }
    }
    else if (light.light_type == 3)
    {
        light_direction = normalize(light.position - point_position);
        float distance = length(light.position - point_position);
        attenuation = attenuation / (light.attenuation[0] +
                                     light.attenuation[1] * distance +
                                     light.attenuation[2] * distance * distance);
    }

    point_normal = normalize(point_normal);
    diffuse = max(dot(point_normal, -light.direction), 0.0);
    diffuse *= attenuation;
    if (diffuse > 0)
    {
        vec3 view_direction = normalize(view_position - point_position);
        vec3 halfway_direction = normalize(light_direction + view_direction);
        specular = max(dot(point_normal, halfway_direction), 0.0);
        specular = specular_strength * pow(specular, shininess);
    }

    return light.color * (diffuse + specular);
}

in vec3 color;
in vec3 position;
in vec3 normal;
out vec4 frag_color;

void main()
{
    vec3 total = vec3(0., 0., 0.);
    vec3 ambient = vec3(0.0);
    for (int i = 0; i < lights.length(); ++i)
    {
        if (lights[i].light_type == 1)
        {
            ambient += lights[i].color;
        }
        else
        {
            total += light_calc(lights[i], position, normal);
        }
    }
    vec3 final_color = color;
    final_color *= total;
    //tone mapping
    if (use_tone_mapping)
    {
        final_color = final_color / (final_color + vec3(1.0));
    }
    //gamma correction
    if (use_gamma_correction)
    {
        final_color = pow(final_color, vec3(1.0/2.2));
    }
    frag_color = vec4(final_color, 1.0);
}
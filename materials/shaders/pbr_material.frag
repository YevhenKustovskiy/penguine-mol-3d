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

// Material parameters
uniform float metallic;
uniform float roughness;
uniform float ao;
const float PI = 3.14159265359;

uniform bool use_tone_mapping;
uniform bool use_gamma_correction;

// Physics based calculations
// Trowbridge-Reitz GGX normal distribution function: statistically approximates
// the relative surface area of microfacets exactly aligned to the halway vector
float DistributionGGX(vec3 normal, vec3 halfway_direction, float roughness)
{
    float a = roughness*roughness;
    float a2 = a*a;
    float NdotH = max(dot(normal, halfway_direction), 0.0);
    float NdotH2 = NdotH*NdotH;

    float nom   = a2;
    float denom = (NdotH2 * (a2 - 1.0) + 1.0);
    denom = PI * denom * denom;

    return nom / denom;
}

// Schlick-Beckmann approximation geometry function: statistically approximates
// the relative surface area where its microsurface details overshadow each other
// causing light rays to be occluded
float GeometrySchlickGGX(float NdotV, float roughness)
{
    float r = (roughness + 1.0);
    float k = (r*r) / 8.0;

    float nom   = NdotV;
    float denom = NdotV * (1.0 - k) + k;

    return nom / denom;
}

// Smith's method
float GeometrySmith(vec3 normal, vec3 view_direction, vec3 light_direction, float roughness)
{
    float NdotV = max(dot(normal, view_direction), 0.0);
    float NdotL = max(dot(normal, light_direction), 0.0);
    float ggx2 = GeometrySchlickGGX(NdotV, roughness);
    float ggx1 = GeometrySchlickGGX(NdotL, roughness);

    return ggx1 * ggx2;
}

// Fresnel-Schlick approximation of Fresnel equation: decribes the ratio of light that gets
// reflected over the light that gets refracted (F0 == normal incidence)
vec3 fresnelSchlick(float cosTheta, vec3 F0)
{
    return F0 + (1.0 - F0) * pow(clamp(1.0 - cosTheta, 0.0, 1.0), 5.0);
}

vec3 light_calc(Light light, vec3 albedo, vec3 point_position, vec3 point_normal, vec3 view_direction, vec3 F0)
{
    float attenuation = 1.0;
    float distance = length(light.position - point_position);
    vec3 light_direction = vec3(0.0, 0.0, 0.0);

    if (light.light_type == 2)
    {
        light_direction = -normalize(light.direction);
        if (use_gamma_correction)
        {
            attenuation = attenuation / (distance * distance);
        }
        else
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

    vec3 halfway_direction = normalize(light_direction + view_direction);
    vec3 radiance = light.color * attenuation;

    float NDF = DistributionGGX(point_normal, halfway_direction, roughness);
    float G = GeometrySmith(point_normal, view_direction, light_direction, roughness);
    vec3 F = fresnelSchlick(clamp(dot(halfway_direction, view_direction),0.0, 1.0), F0);

    vec3 kS = F;
    vec3 kD = vec3(1.0) - kS;
    kD *= 1.0 - metallic;

    vec3 numerator = NDF * G * F;
    float denominator = 4.0 * max(dot(point_normal, view_direction), 0.0)
    * max(dot(point_normal, light_direction), 0.0) + 0.0001;
    vec3 specular = numerator / denominator;

    float NdotL = max(dot(point_normal, light_direction), 0.0);

    return (kD * albedo / PI + specular) * radiance * NdotL;
}

in vec3 color;
in vec3 position;
in vec3 normal;
out vec4 frag_color;

void main()
{
    vec3 albedo = color;
    vec3 point_normal = normalize(normal);
    vec3 view_direction = normalize(view_position-position);
    vec3 Lo = vec3(0.0);
    vec3 F0 = vec3(0.04);
    F0 = mix(F0, albedo, metallic);
    vec3 ambient = vec3(0.0);
    for (int i = 0; i < lights.length(); ++i)
    {
        if (lights[i].light_type == 1)
        {
            ambient += lights[i].color;
        }
        else
        {
            Lo += light_calc(lights[i], albedo, position, point_normal, view_direction, F0);
        }
    }
    ambient = ambient * albedo * ao;
    vec3 final_color = ambient + Lo;

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
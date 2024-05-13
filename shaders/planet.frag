#version 330 core
out vec4 FragColor;

in vec3 Normal;  
in vec3 FragPos;  
in vec3 Position;

uniform samplerCube surfaceTexture;

uniform float object;

// PRM reflectance coefficents
const float ambientStrength = 0.1;
const float diffuseStrength = 0.8;
const float specularStrength = 0.5;
const float shininess = 32.0;

// Light positions
uniform vec3 viewPos; 
uniform vec3 sunPos;
uniform vec3 sunColor;
uniform vec3 lightPos; 
uniform vec3 lightColor;


vec3 getLight(vec3 color, vec3 pos) {
    // ambient
    vec3 ambient = ambientStrength * color;
    
    // diffuse 
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(pos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * color;
    
    // specular
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);  
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    vec3 specular = specularStrength * spec * color;  
    return (ambient + diffuse + specular);
}

vec3 applyLight(vec3 objectColor){
    
        
    vec3 totalLight = (getLight(sunColor, sunPos) + getLight(lightColor, lightPos)) / 2;
    totalLight /= 2;
    return totalLight * objectColor;
}


void main()
{
    vec4 objectColor = texture(surfaceTexture, Position);

    if (object == 2.0) {  
        
        FragColor = vec4(applyLight(objectColor.rgb), 1.0);
    } 
    else {
        FragColor = objectColor;
    }
} 
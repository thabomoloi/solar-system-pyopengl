#version 330 core
out vec4 FragColor;

in vec3 Normal;  
in vec3 FragPos;  
in vec3 Position;

uniform samplerCube surfaceTexture;

uniform vec3 lightPos; 
uniform vec3 viewPos; 
uniform vec3 lightColor;
uniform float object;

void main()
{
    vec3 objectColor = vec3(texture(surfaceTexture, Position));
    if (object == 2.0) {  
        // ambient
        float ambientStrength = 0.15;
        vec3 ambient = ambientStrength * lightColor;
        
        // diffuse 
        vec3 norm = normalize(Normal);
        vec3 lightDir = normalize(lightPos - FragPos);
        float diff = max(dot(norm, lightDir), 0.0);
        vec3 diffuse = diff * lightColor;
        
        // specular
        float specularStrength = 0.625;
        vec3 viewDir = normalize(viewPos - FragPos);
        vec3 reflectDir = reflect(-lightDir, norm);  
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
        vec3 specular = specularStrength * spec * lightColor;  
            
        vec3 result = (ambient + diffuse + specular) * objectColor;
        FragColor = vec4(result, 1.0);
    } 
    else {
        FragColor = texture(surfaceTexture, Position);
    }
} 
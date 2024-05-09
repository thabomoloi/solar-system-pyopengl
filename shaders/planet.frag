#version 330 core

in vec3 textureCoord;

uniform samplerCube sphere;

out vec4 FragColor;
void main()
{
    FragColor = texture(sphere, textureCoord);
}
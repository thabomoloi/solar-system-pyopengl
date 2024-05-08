#version 330 core

in vec2 fragTextureCoord;

uniform sampler2D planetTexture;

out vec4 color;

void main()
{
    color = texture(planetTexture, fragTextureCoord);
}

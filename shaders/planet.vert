#version 330 core

layout(location = 0) in vec3 positionCoord;
layout(location = 1) in vec2 textureCoord;

uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

out vec2 fragTextureCoord;

void main()
{
    gl_Position = projection * view * model * vec4(positionCoord, 1.0);
    fragTextureCoord = textureCoord;
}

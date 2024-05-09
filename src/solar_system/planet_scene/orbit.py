import numpy as np
from OpenGL.GL import *

from solar_system.constants import *


class Orbit:
    def __init__(self, semi_major_axis: float, eccentricity: float, shader):
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.shader = shader

        self.color = (1.0, 1.0, 1.0)

        self.vertices = self.create()
        self.vertexCount = len(self.vertices) // 3
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(
            GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW
        )

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    def cleanup(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))

    def create(self):
        vertices = []
        num_points = 360
        for i in range(num_points):
            angle = 2 * np.pi * i / num_points
            x = self.semi_major_axis * (np.cos(angle) - self.eccentricity)
            z = self.semi_major_axis * np.sin(angle)
            vertices.extend([x, 0, z, *self.color])
        return vertices

    def render(self):
        glUseProgram(self.shader)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount)

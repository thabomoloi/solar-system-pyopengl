import numpy as np
from OpenGL.GL import *
from Geometry import Geometry
from constants import *
from helpers import *


class CelestialObject(Geometry):
    sphere_shader = None

    def __init__(self, size):
        super().__init__(SPHERE_FILE)
        self.size = size
        self.name = "SUN"

    def render(self):
        color_location = glGetUniformLocation(
            CelestialObject.sphere_shader, "objectColor"
        )

        glUniform3f(color_location, *COLORS[self.name])

        model_location = glGetUniformLocation(CelestialObject.sphere_shader, "model")
        glUniformMatrix4fv(model_location, 1, GL_FALSE, self.size)

        self.draw()


class Orbit:
    def __init__(self, semi_major_axis: float, eccentricity: float):
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity

        self.vertices = self.create()
        self.vertexCount = len(self.vertices) // 3
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.color = (1.0, 1.0, 1.0)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(
            GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW
        )
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

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
            vertices.extend([x, 0, z])
        return vertices

    def render(self):
        shader = CelestialObject.sphere_shader
        glUseProgram(shader)
        glBindVertexArray(self.vao)
        glUniform3f(glGetUniformLocation(shader, "objectColor"), *self.color)
        glDrawArrays(GL_LINE_LOOP, 0, self.vertexCount)


class MovingObject(CelestialObject):
    def __init__(
        self,
        name: str,
        size,
        semi_major_axis: float = 0,
        eccentricity: float = 0,
        orbit_period: float = 0,
    ) -> None:
        super().__init__(size)
        self.name = name
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.orbit_period = orbit_period
        self.angle = 0
        self.orbit = Orbit(semi_major_axis, eccentricity)

    @property
    def position(self):
        x = self.semi_major_axis * (np.cos(self.angle) - self.eccentricity)
        y = 0
        z = (
            self.semi_major_axis
            * np.sqrt(1 - self.eccentricity**2)
            * np.sin(self.angle)
        )
        return np.array([x, y, z])

    def render(self):
        self.orbit.render()
        self.size = translate_object(SIZES[self.name], self.position)
        self.angle += 2 * np.pi / self.orbit_period
        if self.angle > 2 * np.pi:
            self.angle -= 2 * np.pi
        super().render()

    def cleanup(self):
        self.orbit.cleanup()
        super().cleanup()

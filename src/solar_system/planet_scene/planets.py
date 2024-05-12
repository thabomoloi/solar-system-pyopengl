import numpy as np
from typing import Literal
from OpenGL.GL import *
from solar_system.constants import *
from solar_system.helpers import *
from solar_system.planet_scene.celestial_object import CelestialObject


class MovingObject(CelestialObject):
    speed: int = 0.01

    def __init__(
        self,
        shader,
        name: str,
        size,
        semi_major_axis: float = 0,
        eccentricity: float = 0,
        orbit_period: float = 0,
        inclination_angle: float = 0,
        rotation_period: float = 0,
        rotation_direction: Literal["anticlockwise", "clockwise"] = "anticlockwise",
    ) -> None:
        super().__init__(size, name, shader)
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.orbit_period = orbit_period
        self.angle = 0
        self.rotation_angle = 0
        self.inclination_angle = np.radians(inclination_angle)
        self.rotation_period = rotation_period
        self.rotation_direction = rotation_direction

    @classmethod
    def set_speed(cls, value: int):
        if value > 0:
            cls.speed = value
        else:
            cls.speed = 0

    @property
    def position(self):
        return self.calculate_position()

    def calculate_position(self):
        x = -self.semi_major_axis * (np.cos(self.angle) - self.eccentricity)
        y = 0
        z = (
            self.semi_major_axis
            * np.sqrt(1 - self.eccentricity**2)
            * np.sin(self.angle)
        )
        return np.array([x, y, z])

    def render(self):
        # Set the lightPos uniform to (0,0,0)
        light_pos = [0.0, 0.0, 0.0]
        glUniform3fv(glGetUniformLocation(self.sphere_shader, "lightPos"), 1, light_pos)

        if self.rotation_direction == "anticlockwise":
            self.rotation_angle -= 2 * np.pi * MovingObject.speed / self.rotation_period
            if self.rotation_angle < -2 * np.pi:
                self.rotation_angle += 2 * np.pi
        else:
            self.rotation_angle += 2 * np.pi * MovingObject.speed / self.rotation_period
            if self.rotation_angle > 2 * np.pi:
                self.rotation_angle -= 2 * np.pi

        # Calculate rotation matrices for inclination and rotation
        inclination_rotation = pyrr.Matrix44.from_z_rotation(self.inclination_angle)
        self_rotation = pyrr.Matrix44.from_y_rotation(self.rotation_angle)

        # Combine the rotation matrices
        rotation_matrix = inclination_rotation * self_rotation

        self.size = translate_object(SIZES[self.name], self.position)
        self.size = np.dot(rotation_matrix, self.size)
        self.angle += 2 * np.pi * MovingObject.speed / self.orbit_period
        if self.angle > 2 * np.pi:
            self.angle -= 2 * np.pi

        super().render()


class Planet(MovingObject):
    def __init__(
        self,
        shader,
        name: str,
        size,
        semi_major_axis: float = 0,
        eccentricity: float = 0,
        orbit_period: float = 0,
        inclination_angle: float = 0,
        rotation_period: float = 0,
        rotation_direction: Literal["anticlockwise", "clockwise"] = "anticlockwise",
    ) -> None:
        super().__init__(
            shader,
            name,
            size,
            semi_major_axis,
            eccentricity,
            orbit_period,
            inclination_angle,
            rotation_period,
            rotation_direction,
        )


class Moon(MovingObject):
    def __init__(
        self,
        shader,
        name: str,
        size,
        semi_major_axis: float = 0,
        eccentricity: float = 0,
        orbit_period: float = 0,
        inclination_angle: float = 0,
        rotation_period: float = 0,
        planet: Planet = None,
    ) -> None:
        super().__init__(
            shader,
            name,
            size,
            semi_major_axis,
            eccentricity,
            orbit_period,
            inclination_angle,
            rotation_period,
        )
        self.planet = planet

    @property
    def position(self):
        return self.planet.position + self.calculate_position()


class Sun(CelestialObject):
    speed: int = 0.01

    def __init__(self, shader, size):
        super().__init__(size, "SUN", shader)
        self.rotation_angle = 0
        self.rotation_period = 38
        self.inclination_angle = np.radians(7.25)

    @classmethod
    def set_speed(cls, value: int):
        if value > 0:
            cls.speed = value
        else:
            cls.speed = 0

    def render(self):
        self.rotation_angle -= 2 * np.pi * Sun.speed / self.rotation_period
        if self.rotation_angle < -2 * np.pi:
            self.rotation_angle += 2 * np.pi

        # Calculate rotation matrices for inclination and rotation
        inclination_rotation = pyrr.Matrix44.from_z_rotation(self.inclination_angle)
        self_rotation = pyrr.Matrix44.from_y_rotation(self.rotation_angle)

        # Combine the rotation matrices
        rotation_matrix = inclination_rotation * self_rotation

        self.size = translate_object(SIZES[self.name], np.array([0, 0, 0]))
        self.size = np.dot(rotation_matrix, self.size)

        super().render()

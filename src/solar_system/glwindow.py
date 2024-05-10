from typing import Literal
from solar_system.constants import *
from solar_system.helpers import *
import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr
from solar_system.planet_scene.planets import Sun, Moon, Planet, MovingObject


class OpenGLWindow:

    def __init__(self):
        self.clock = pg.time.Clock()
        self.sun = None
        self.planets = []
        self.moon = None
        self.speed = 0.01
        self.speed_step = 0.01
        self.camera_position = pyrr.Vector3([0.0, 0.0, -10.0])
        self.camera_target = pyrr.Vector3([0.0, 0.0, 0.0])
        self.camera_up = pyrr.Vector3([0.0, 1.0, 0.0])
        self.camera_distance = 10.0  # Initial distance from target
        self.camera_pitch = 0.0  # Initial pitch angle
        self.camera_yaw = 0.0  # Initial yaw angle
        self.camera_roll = 0.0
        self.fov = 90
        self.screen_width = (0,)
        self.screen_height = (0,)

    def update_speeds(self):
        Sun.set_speed(self.speed)
        MovingObject.set_speed(self.speed)

    def increase_speed(self):
        self.speed += self.speed_step
        self.update_speeds()

    def decrease_speed(self):
        self.speed -= self.speed_step
        if self.speed < 0:
            self.speed = 0
        self.update_speeds()

    def zoom_in(self):
        self.fov -= 15
        if self.fov < 0:
            self.fov = 0

    def zoom_out(self):
        self.fov += 15
        if self.fov > 360:
            self.fov = 360

    def setup_camera(self, shader):
        projection = pyrr.matrix44.create_perspective_projection(
            fovy=self.fov,
            aspect=self.screen_width / self.screen_height,
            near=0.1,
            far=75,
            dtype=np.float32,
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),
            1,
            GL_FALSE,
            projection,
        )

        # Convert camera orientation angles to rotation matrices
        rotation_x = pyrr.Matrix44.from_x_rotation(self.camera_pitch)
        rotation_y = pyrr.Matrix44.from_y_rotation(self.camera_yaw)
        rotation_z = pyrr.Matrix44.from_z_rotation(self.camera_roll)

        # Combine the rotation matrices to get the final orientation matrix
        orientation_matrix = rotation_x * rotation_y * rotation_z

        # Calculate the camera position based on the orientation and distance from target
        camera_position = self.camera_target + orientation_matrix * pyrr.Vector3(
            [0.0, 0.0, -self.camera_distance]
        )

        camera_up = rotation_z * self.camera_up
        # Create the view matrix using the calculated camera position, target, and up vector
        view_matrix = pyrr.matrix44.create_look_at(
            camera_position,
            target=self.camera_target,
            up=camera_up,
            dtype=np.float32,
        )

        # Set the view matrix in the shader
        glUniformMatrix4fv(
            glGetUniformLocation(shader, "view"),
            1,
            GL_FALSE,
            view_matrix,
        )

    def rotate_camera(
        self,
        axis: Literal["x", "y", "z"],
        direction: Literal["clockwise", "anticlockwise"] = "clockwise",
    ):

        step = np.pi / 90  # Convert 1 degree to radians

        if axis == "x":
            if direction == "clockwise":
                self.camera_pitch += step
            else:
                self.camera_pitch -= step
        elif axis == "y":
            if direction == "clockwise":
                self.camera_yaw += step
            else:
                self.camera_yaw -= step
        else:
            if direction == "clockwise":
                self.camera_roll += step
            else:
                self.camera_roll -= step

    def loadShaderProgram(self, vertex, fragment):
        with open(vertex, "r") as f:
            vertex_src = f.readlines()

        with open(fragment, "r") as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER),
        )

        return shader

    def initGL(self, screen_width=640, screen_height=480):
        self.screen_width = screen_width
        self.screen_height = screen_height

        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
        )

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 2)

        pg.display.set_mode((screen_width, screen_height), pg.OPENGL | pg.DOUBLEBUF)

        glEnable(GL_DEPTH_TEST)
        # Uncomment these two lines when perspective camera has been implemented
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glClearColor(0, 0, 0, 1)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Note that this path is relative to your working directory when running the program
        # You will need change the filepath if you are running the script from inside ./src/

        self.shader = self.loadShaderProgram(
            "./shaders/planet.vert", "./shaders/planet.frag"
        )
        # glUseProgram(self.shader)
        glUseProgram(self.shader)
        self.setup_camera(self.shader)

        self.sun = Sun(self.shader, SIZES["SUN"])

        for name, details in PLANETS.items():
            planet = Planet(self.shader, *details)
            if name == "EARTH":
                self.moon = Moon(self.shader, *MOON, planet)
            self.planets.append(planet)

        print("Setup complete!")

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.setup_camera(self.shader)

        self.sun.render()
        self.moon.render()
        for planet in self.planets:
            planet.render()

        # Swap the front and back buffers on the window, effectively putting what we just "drew"
        # Onto the screen (whereas previously it only existed in memory)
        pg.display.flip()

    def cleanup(self):
        glDeleteVertexArrays(1, (self.vao,))
        self.sun.cleanup()
        self.moon.cleanup()
        for planet in self.planets:
            planet.cleanup()

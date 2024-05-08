from constants import *
from helpers import *
import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr
from planets import CelestialObject, MovingObject


class OpenGLWindow:

    def __init__(self):
        self.triangle = None
        self.clock = pg.time.Clock()
        self.sun = None
        self.earth = None
        self.moon = None
        self.speed = 1.0
        self.rotation_x = 0.0
        self.rotation_y = 0.0

        self.camera_position = pyrr.Vector3([0.0, 0.0, -10.0])
        self.camera_target = pyrr.Vector3([0.0, 0.0, 0.0])
        self.camera_up = pyrr.Vector3([0.0, 1.0, 0.0])
        self.camera_distance = 10.0  # Initial distance from target
        self.camera_pitch = 0.0  # Initial pitch angle
        self.camera_yaw = 0.0  # Initial yaw angle

    # Your existing code...

    def setup_camera(self, shader):
        view = pyrr.matrix44.create_look_at(
            self.camera_position,
            target=self.camera_target,
            up=self.camera_up,
            dtype=np.float32,
        )

        glUniformMatrix4fv(
            glGetUniformLocation(shader, "view"),
            1,
            GL_FALSE,
            view,
        )

    def rotate_camera(self, direction):
        step = 1.0  # Increment for camera rotation
        if direction == "up":
            self.camera_pitch += step
        elif direction == "down":
            self.camera_pitch -= step
        elif direction == "left":
            self.camera_yaw += step
        elif direction == "right":
            self.camera_yaw -= step

        # Calculate new camera position based on pitch and yaw
        self.camera_position[0] = self.camera_target[0] + self.camera_distance * np.cos(
            np.radians(self.camera_pitch)
        ) * np.sin(np.radians(self.camera_yaw))
        self.camera_position[1] = self.camera_target[1] + self.camera_distance * np.sin(
            np.radians(self.camera_pitch)
        )
        self.camera_position[2] = self.camera_target[2] + self.camera_distance * np.cos(
            np.radians(self.camera_pitch)
        ) * np.cos(np.radians(self.camera_yaw))

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
        pg.init()

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
            "./shaders/simple.vert", "./shaders/simple.frag"
        )
        glUseProgram(self.shader)

        # colorLoc = glGetUniformLocation(self.shader, "objectColor")
        # glUniform3f(colorLoc, 1.0, 1.0, 1.0)
        # glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

        # Uncomment this for triangle rendering
        # self.triangle = Triangle(self.shader)

        # Uncomment this for model rendering
        # self.cube = Geometry('./resources/cube.obj')

        projection = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=640 / 480, near=0.1, far=100, dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"),
            1,
            GL_FALSE,
            projection,
        )

        CelestialObject.sphere_shader = self.shader

        self.earth = MovingObject(*EARTH)
        self.moon = MovingObject(*MOON)
        self.sun = CelestialObject(SIZES["SUN"])

        print("Setup complete!")

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shader)  # You may not need this line

        self.setup_camera(self.shader)
        print("earth")

        # Uncomment this for triangle rendering
        # glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertexCount)

        # Uncomment this for model rendering
        # glDrawArrays(GL_TRIANGLES, 0, self.cube.vertexCount)
        # glDrawArrays(GL_TRIANGLES, 0, self.sphere.vertexCount)

        self.sun.render()
        self.earth.render()
        self.moon.render()

        # Swap the front and back buffers on the window, effectively putting what we just "drew"
        # Onto the screen (whereas previously it only existed in memory)
        pg.display.flip()

    def cleanup(self):
        glDeleteVertexArrays(1, (self.vao,))
        # Uncomment for triangle rendering
        # self.triangle.cleanup()
        # Uncomment for model rendering
        # self.cube.cleanup()
        self.sun.cleanup()
        self.earth.cleanup()
        self.moon.cleanup()

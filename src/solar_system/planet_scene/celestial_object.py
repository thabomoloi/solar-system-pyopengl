from OpenGL.GL import *
from solar_system.geometry import Geometry
from solar_system.constants import *
from solar_system.helpers import *
from PIL import Image


class CelestialObject(Geometry):

    def __init__(self, size, name: str = "SUN", shader=None):
        super().__init__(SPHERE_FILE)
        self.size = size
        self.name = name
        self.sphere_shader = shader
        self.texture_id = self.load_texture(f"textures/{self.name.lower()}.png")

    def load_texture(self, filename: str):
        image = Image.open(filename)
        width, _ = image.size
        face_width = width // 4  # Each face has width equal to 1/4th of the image width

        # Convert the image to RGB mode
        image = image.convert("RGB")

        # Extract each face from the image
        faces = [
            (
                image.crop((face_width * 2, face_width, face_width * 3, face_width * 2))
                .rotate(180)
                .transpose(Image.FLIP_LEFT_RIGHT),
                GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
            ),  # Right face
            (
                image.crop((0, face_width, face_width, face_width * 2))
                .rotate(180)
                .transpose(Image.FLIP_LEFT_RIGHT),
                GL_TEXTURE_CUBE_MAP_POSITIVE_X,
            ),  # Left face
            (
                image.crop((face_width, 0, face_width * 2, face_width)).transpose(
                    Image.FLIP_LEFT_RIGHT
                ),
                GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
            ),  # Top face
            (
                image.crop(
                    (face_width, face_width * 2, face_width * 2, face_width * 3)
                ).transpose(Image.FLIP_LEFT_RIGHT),
                GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
            ),  # Bottom face
            (
                image.crop(
                    (face_width * 3, face_width, face_width * 4, face_width * 2)
                ).transpose(Image.FLIP_TOP_BOTTOM),
                GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
            ),  # Back face
            (
                image.crop((face_width, face_width, face_width * 2, face_width * 2))
                .rotate(180)
                .transpose(method=Image.FLIP_LEFT_RIGHT),
                GL_TEXTURE_CUBE_MAP_NEGATIVE_Z,
            ),  # Front face
        ]

        # Convert the faces to OpenGL texture format
        cube_map_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, cube_map_texture)

        for face, texture in faces:
            face_data = face.tobytes("raw", "RGB", 0, -1)
            glTexImage2D(
                texture,
                0,
                GL_RGB,
                face_width,
                face_width,
                0,
                GL_RGB,
                GL_UNSIGNED_BYTE,
                face_data,
            )

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

        return cube_map_texture

    def render(self):
        glUseProgram(self.sphere_shader)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture_id)

        model_location = glGetUniformLocation(self.sphere_shader, "model")
        glUniformMatrix4fv(model_location, 1, GL_FALSE, self.size)

        self.draw()

    def cleanup(self):
        super().cleanup()
        glDeleteTextures(1, (self.texture_id,))

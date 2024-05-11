from typing import Literal
from solar_system.geometry import Geometry
from solar_system.constants import *
from OpenGL.GL import *
from PIL import Image
import numpy as np

from typing import Literal
from solar_system.geometry import Geometry
from solar_system.constants import *
from OpenGL.GL import *
from PIL import Image
import numpy as np


def get_cube_face(
    image: Image.Image,
    orientation: Literal["right", "left", "top", "bottom", "back", "front"],
    face_width: int,
) -> Image:
    """Returns a cube face from an image.

    Args:
        image (Image): Image containing six cube faces.
        orientation (Literal["right", "left", "top", "bottom", "back", "front"]): Orientation of the cube face.
        face_width (int): The width of the cube face.

    Raises:
        ValueError: Invalid orientation if unexpected value.

    Returns:
        Image: An image of a single cube face.
    """
    orientation_mapping = {
        "right": (face_width * 2, face_width, face_width * 3, face_width * 2),
        "left": (0, face_width, face_width, face_width * 2),
        "top": (face_width, 0, face_width * 2, face_width),
        "bottom": (face_width, face_width * 2, face_width * 2, face_width * 3),
        "back": (face_width * 3, face_width, face_width * 4, face_width * 2),
        "front": (face_width, face_width, face_width * 2, face_width * 2),
    }

    if orientation in orientation_mapping:
        image = image.crop(orientation_mapping[orientation])
        if orientation not in ["top", "bottom"]:
            return image.rotate(180)
        return image
    else:
        raise ValueError(f"Invalid orientation: found {orientation}.")


def use_cubemap(filepath: str):
    image = Image.open(filepath)
    width, _ = image.size

    # Each face has width equal to 1/4th of the image width
    face_width = width // 4

    image = image.convert("RGB")

    orientation = ["right", "left", "top", "bottom", "back", "front"]
    texture_faces = [get_cube_face(image, x, face_width) for x in orientation]

    for i, face in enumerate(texture_faces):
        face_data = face.tobytes("raw", "RGB", 0, -1)
        glTexImage2D(
            GL_TEXTURE_CUBE_MAP_POSITIVE_X + i,
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


class Stars(Geometry):
    def __init__(self, shader=None):
        super().__init__(CUBE_FILE)
        self.name = "STARS"
        self.shader = shader
        self.size = SIZES[self.name]
        self.texture_id = self.load_texture(f"textures/{self.name.lower()}.png")

    def load_texture(self, filepath: str):
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, texture_id)
        use_cubemap(filepath)
        return texture_id

    def render(self):

        glDepthMask(GL_FALSE)
        glDisable(GL_CULL_FACE)
        glUseProgram(self.shader)

        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture_id)

        model_location = glGetUniformLocation(self.shader, "model")
        glUniformMatrix4fv(model_location, 1, GL_FALSE, self.size)

        super().draw()
        glEnable(GL_CULL_FACE)
        glDepthMask(GL_TRUE)

    def cleanup(self):
        # glDeleteVertexArrays(1, (self.vao,))
        # glDeleteBuffers(1, (self.vbo,))
        super().cleanup()
        glDeleteTextures(1, (self.texture_id,))

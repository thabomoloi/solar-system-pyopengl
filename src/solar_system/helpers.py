import pyrr
import numpy as np
from OpenGL.GL import *


def translate_object(size, postion):
    return pyrr.matrix44.multiply(
        size,
        pyrr.matrix44.create_from_translation(postion, dtype=np.float32),
    )


# def setup_camera(shader):
#     glUniformMatrix4fv(
#         glGetUniformLocation(shader, "view"),
#         1,
#         GL_FALSE,
#         pyrr.matrix44.create_look_at(
#             pyrr.Vector3([0.0, 0.0, -10]),
#             target=pyrr.Vector3([0.0, 0.0, 0.0]),
#             up=pyrr.Vector3([0.0, 1.0, 0.0]),
#             dtype=np.float32,
#         ),
#     )

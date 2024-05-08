from OpenGL.GL import *
import pygame as pg


class Cubemap:
    def __init__(self, filenames: list[str]) -> None:
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture_id)
        self.load_textures(filenames)

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

    def load_textures(filenames: list[str]):
        for i, filename in enumerate(filenames):
            img = pg.image.load(filename)
            img_data = pg.image.tostring(img, "RGBA", 1)

            # Check image dimensions
            width, height = img.get_width(), img.get_height()
            if width != height:
                raise ValueError(
                    f"Image dimensions must be equal for a cubemap face (got {width}x{height} for {filename})"
                )

            glTexImage2D(
                GL_TEXTURE_CUBE_MAP_POSITIVE_X + i,
                0,
                GL_RGBA,
                width,
                height,
                0,
                GL_RGBA,
                GL_UNSIGNED_BYTE,
                img_data,
            )

    def cleanup(self):
        glDeleteTextures(1, (self.textures,))

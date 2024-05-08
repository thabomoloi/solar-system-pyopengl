import os

os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

import pygame as pg
from GLWindow import *


def main():
    window = OpenGLWindow()
    window.initGL()
    running = True
    paused = False
    speed = 1.0  # Initial speed

    clock = pg.time.Clock()  # Create a clock object to control the frame rate
    while running:
        clock.tick(60)

        if not paused:
            window.render()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    window.rotate_camera("up")
                elif event.key == pg.K_DOWN:
                    window.rotate_camera("down")
                elif event.key == pg.K_LEFT:
                    window.rotate_camera("left")
                elif event.key == pg.K_RIGHT:
                    window.rotate_camera("right")

    pg.quit()


if __name__ == "__main__":
    main()

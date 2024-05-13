import os

os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

import pygame as pg
from solar_system.glwindow import OpenGLWindow


def main():
    pg.init()
    # Get display info
    info = pg.display.Info()

    # Get screen width and height
    screen_height = info.current_h - 128
    screen_width = screen_height

    window = OpenGLWindow()
    window.initGL(screen_width=screen_width, screen_height=screen_height)
    running = True
    paused = False

    clock = pg.time.Clock()  # Create a clock object to control the frame rate

    while running:
        clock.tick(60)
        window.render()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_x and pg.key.get_mods() & pg.KMOD_CTRL:
                    window.rotate_camera("x", "anticlockwise")
                elif event.key == pg.K_x:
                    window.rotate_camera("x", "clockwise")
                elif event.key == pg.K_y and pg.key.get_mods() & pg.KMOD_CTRL:
                    window.rotate_camera("y", "anticlockwise")
                elif event.key == pg.K_y:
                    window.rotate_camera("y", "clockwise")
                elif event.key == pg.K_z and pg.key.get_mods() & pg.KMOD_CTRL:
                    window.rotate_camera("z", "anticlockwise")
                elif event.key == pg.K_z:
                    window.rotate_camera("z", "clockwise")
                elif event.key == pg.K_UP and pg.key.get_mods() & pg.KMOD_CTRL:
                    window.zoom_in()
                elif event.key == pg.K_DOWN and pg.key.get_mods() & pg.KMOD_CTRL:
                    window.zoom_out()
                elif event.key == pg.K_UP:
                    window.increase_speed()
                elif event.key == pg.K_DOWN:
                    window.decrease_speed()
                elif event.key == pg.K_SPACE:
                    if not paused:
                        window.speed = 0
                        window.update_speeds()
                    else:
                        window.increase_speed()
                    paused = not paused

    pg.quit()


if __name__ == "__main__":
    main()

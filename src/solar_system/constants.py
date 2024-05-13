import pyrr

SPHERE_FILE = "./resources/sphere.obj"
CUBE_FILE = "./resources/cube.obj"


SIZE_VECTORS = {
    "SUN": [0.75] * 3,
    "MERCURY": [0.2] * 3,
    "VENUS": [0.3] * 3,
    "EARTH": [0.325] * 3,
    "MARS": [0.275] * 3,
    "JUPITER": [0.5] * 3,
    "SATURN": [0.4] * 3,
    "URANUS": [0.35] * 3,
    "NEPTUNE": [0.35] * 3,
    "MOON": [0.1] * 3,
    "STARS": [15] * 3,
}


SIZES = {
    "SUN": pyrr.matrix44.create_from_scale(SIZE_VECTORS["SUN"]),
    "MERCURY": pyrr.matrix44.create_from_scale(SIZE_VECTORS["MERCURY"]),
    "VENUS": pyrr.matrix44.create_from_scale(SIZE_VECTORS["VENUS"]),
    "EARTH": pyrr.matrix44.create_from_scale(SIZE_VECTORS["EARTH"]),
    "MARS": pyrr.matrix44.create_from_scale(SIZE_VECTORS["MARS"]),
    "JUPITER": pyrr.matrix44.create_from_scale(SIZE_VECTORS["JUPITER"]),
    "SATURN": pyrr.matrix44.create_from_scale(SIZE_VECTORS["SATURN"]),
    "URANUS": pyrr.matrix44.create_from_scale(SIZE_VECTORS["URANUS"]),
    "NEPTUNE": pyrr.matrix44.create_from_scale(SIZE_VECTORS["NEPTUNE"]),
    "MOON": pyrr.matrix44.create_from_scale(SIZE_VECTORS["MOON"]),
    "STARS": pyrr.matrix44.create_from_scale(SIZE_VECTORS["STARS"]),
}


MERCURY = ("MERCURY", SIZES["MERCURY"], 1.25, 0, 87.969, 2, 58.646)
VENUS = ("VENUS", SIZES["VENUS"], 2.25, 0, 224.701, 177, 243.025, "clockwise")
EARTH = ("EARTH", SIZES["EARTH"], 3.5, 0, 365.256, 23.5, 0.997)
MARS = ("MARS", SIZES["MARS"], 4.75, 0, 686.980, 25, 1.027)
JUPITER = ("JUPITER", SIZES["JUPITER"], 6, 0, 4332.589, 3.13, 0.41354)
SATURN = ("SATURN", SIZES["SATURN"], 7.25, 0, 10759.22, 26.7, 0.44401)
URANUS = ("URANUS", SIZES["URANUS"], 8.25, 0, 30688.5, 97.77, 0.71833, "clockwise")
NEPTUNE = ("NEPTUNE", SIZES["NEPTUNE"], 9.25, 0, 60182.0, 28, 0.67125)
MOON = ("MOON", SIZES["MOON"], 0.55, 0, 27.322, 5.145, 27.322)

PLANETS = {
    "MERCURY": MERCURY,
    "VENUS": VENUS,
    "EARTH": EARTH,
    "MARS": MARS,
    "JUPITER": JUPITER,
    "SATURN": SATURN,
    "URANUS": URANUS,
    "NEPTUNE": NEPTUNE,
}

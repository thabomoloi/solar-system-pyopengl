import pyrr

SPHERE_FILE = "./resources/sphere.obj"

SIZE_VECTORS = {
    "SUN": [1.5] * 3,
    "MERCURY": [0.5] * 3,
    "VENUS": [0.60] * 3,
    "EARTH": [0.625] * 3,
    "MARS": [0.55] * 3,
    "JUPITER": [1] * 3,
    "SATURN": [0.9] * 3,
    "URANUS": [0.8] * 3,
    "NEPTUNE": [0.775] * 3,
    "MOON": [0.2] * 3,
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
}
COLORS = {
    "SUN": (1, 0.83, 0.50),
    "MERCURY": (0.64, 0.64, 0.64),
    "VENUS": (0.81, 0.75, 0.66),
    "EARTH": (0.29, 0.85, 0.90),
    "MARS": (0.78, 0.39, 0.26),
    "JUPITER": (0.85, 0.67, 0.47),
    "SATURN": (0.90, 0.85, 0.70),
    "URANUS": (0.66, 0.84, 0.85),
    "NEPTUNE": (0.31, 0.51, 0.74),
    "MOON": (0.82, 0.82, 0.82),
}

MERCURY = ("MERCURY", SIZES["MERCURY"], 3, 0.2056, 87.969, 7.005, 58.646)
VENUS = ("VENUS", SIZES["VENUS"], 4, 0.0068, 224.701, 3.39458, -243.025)
EARTH = ("EARTH", SIZES["EARTH"], 6, 0.0167, 365.256, 0.00005, 0.997)
MARS = ("MARS", SIZES["MARS"], 9, 0.0934, 686.980, 1.850, 1.027)
JUPITER = ("JUPITER", SIZES["JUPITER"], 11, 0.0489, 4332.589, 1.304, 0.41354)
SATURN = ("SATURN", SIZES["SATURN"], 16, 0.0565, 10759.22, 2.485, 0.44401)
URANUS = ("URANUS", SIZES["URANUS"], 22, 0.0463, 30688.5, 0.772, -0.71833)
NEPTUNE = (
    "NEPTUNE",
    SIZES["NEPTUNE"],
    29,
    0.0097,
    60182.0,
    1.767975,
    0.67125,
)
MOON = ("MOON", SIZES["MOON"], 1, 0.0549, 27.322, 5.145, 27.322)

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

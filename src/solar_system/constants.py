import pyrr

SPHERE_FILE = "./resources/sphere.obj"
SIZE_VECTORS = {"SUN": [1] * 3, "EARTH": [0.5] * 3, "MOON": [0.15] * 3}
SIZES = {
    "SUN": pyrr.matrix44.create_from_scale(SIZE_VECTORS["SUN"]),
    "EARTH": pyrr.matrix44.create_from_scale(SIZE_VECTORS["EARTH"]),
    "MOON": pyrr.matrix44.create_from_scale(SIZE_VECTORS["MOON"]),
}
COLORS = {
    "SUN": (1, 0.83, 0.50),
    "EARTH": (0.29, 0.85, 0.90),
    "MOON": (0.82, 0.82, 0.82),
}

EARTH = ("EARTH", SIZES["EARTH"], 1.0 * 2, 0.0167, 365.0, 23.45, 1)
MOON = ("MOON", SIZES["MOON"], 0.35 * 2, 0.0549, 27.3, 5.145, 27.3)

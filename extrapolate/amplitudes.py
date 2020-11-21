import numpy as np


def standard(t, a1, b1, a2, b2, p1, b3, p2, c3):
    im = a1 * np.exp(-b1 * t) - a2 * np.exp(-b2 * t)
    re = p1 * np.exp(-b3 * t) - p2 * np.exp(-c3 * t)
    return re + im * 1j

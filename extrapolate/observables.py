import numpy as np


def ds(amplitude):
    return np.real(amplitude) ** 2 + np.imag(amplitude) ** 2


def rho(amplitude):
    return np.real(amplitude) / np.imag(amplitude)

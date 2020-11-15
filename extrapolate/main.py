import numpy as np
import matplotlib.pyplot as plt
from extrapolate.data import dataset, params


def ds_standard(t, a1, b1, a2, b2, p1, b3, p2, c3):
    im = a1 * np.exp(-b1 * t) - a2 * np.exp(-b2 * t)
    re = p1 * np.exp(-b3 * t) - p2 * np.exp(-c3 * t)
    return re ** 2 + im ** 2


def main():
    data = dataset((62.400, 62.600))
    data = data[data["-t"].between(0.5, 2.5)]

    plt.errorbar(data["-t"], data["obs"],
                 yerr=data["total err."], fmt='.', markersize=0.1)

    plt.yscale("log")
    plt.xlabel("$|t|$ (GeV$^{2}$)")
    plt.ylabel(r"$d\sigma/dt$ (mb/GeV$^2$)")
    plt.show()


if __name__ == '__main__':
    main()

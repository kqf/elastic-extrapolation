import iminuit
import numpy as np
import matplotlib.pyplot as plt

from iminuit.cost import LeastSquares
from extrapolate.vis import vis
from extrapolate.data import dataset
from extrapolate.params import Params


def ds(t, a1, b1, a2, b2, p1, b3, p2, c3):
    im = a1 * np.exp(-b1 * t) - a2 * np.exp(-b2 * t)
    re = p1 * np.exp(-b3 * t) - p2 * np.exp(-c3 * t)
    return re ** 2 + im ** 2


def fit(data, pars, func):
    loss = LeastSquares(data["-t"], data["obs"], data["total err."], ds)
    minimizer = iminuit.Minuit(loss, pedantic=False, **pars)
    minimizer.migrad(ncall=10000)

    print()
    print("energy at t\\neq 0", data["s"].min(), data["s"].max())
    print("|t|", data["-t"].min(), data["-t"].max())
    print("chi^2_tot ", minimizer.fval)
    print("chi^2/dof ", minimizer.fval / (len(data) - minimizer.nfit))
    return minimizer


def main():
    data = dataset((62.400, 62.600))
    data = data[data["-t"].between(0.5, 2.5)]
    pars = Params()

    m = fit(data, pars.to_minuit(), ds)
    print(m.params)

    with vis(data, label="pp 62.5 Amaldi"):
        t = data["-t"]
        plt.plot(t, ds(t, **pars.values), label="fit 1")
        plt.plot(t, ds(t, **m.values), label="new")
        plt.legend()


if __name__ == '__main__':
    main()

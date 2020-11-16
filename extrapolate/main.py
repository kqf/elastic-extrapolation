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

    # Print the short summary
    print("energy at t\\neq 0 :", data["s"].min(), data["s"].max())
    print("|t|               :", data["-t"].min(), data["-t"].max())
    print("chi^2_tot         :", minimizer.fval)
    print("chi^2/dof         :", minimizer.fval / (len(data) - minimizer.nfit))

    pars_fitted = Params.from_minuit(minimizer.params)
    print(pars_fitted)
    print(pars_fitted.df)
    return minimizer


def main():
    data = dataset((62.400, 62.600))
    data = data[data["-t"].between(0.5, 2.5)]
    pars = Params.from_dat()

    print("Fit with the same limits")
    m_limits = fit(data, pars.to_minuit(), ds)

    print("Fit with no limits")
    m_no_limits = fit(data, pars.values, ds)

    with vis(data, label="pp 62.5 Amaldi"):
        t = data["-t"]
        plt.plot(t, ds(t, **pars.values), label="initial values")
        plt.plot(t, ds(t, **m_limits.values), label="fit (same limits)")
        plt.plot(t, ds(t, **m_no_limits.values), label="fit (no limits)")
        plt.legend()


if __name__ == '__main__':
    main()

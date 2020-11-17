import iminuit
import numpy as np
import pandas as pd
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


def configs(filename="config/energies.json"):
    df = pd.read_json(filename)
    df = df[df["energy"].str[0] < 100]
    fields = df[["energy", "t", "filename", "process"]]
    return fields.to_dict(orient="records")


def main():
    for config in configs():
        data = dataset(**config)
        pars = Params.from_dat()

        m = fit(data, pars.values, ds)

        label = "{} {}".format(config["process"], config["energy"][0])
        with vis(data, label=label):
            plt.plot(data["-t"], ds(data["-t"], **m.values), label="fit")
            plt.legend()


if __name__ == '__main__':
    main()

import iminuit
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from functools import partial
from iminuit.cost import LeastSquares
from extrapolate.vis import plot
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
    return minimizer


def dump(data, minimizer, label, outfile="output.dat"):
    with open(outfile, "a") as f:
        print(label, file=f)
        print("--------------------", file=f)
        # TODO: Clean this
        msg = "energy at t\\neq 0 :"
        print(msg, data["s"].min(), data["s"].max(), file=f)
        msg = "|t|               :"
        print(msg, data["-t"].min(), data["-t"].max(), file=f)
        msg = "chi^2_tot         :"
        print(msg, minimizer.fval, file=f)
        msg = "chi^2/dof         :"
        print(msg, minimizer.fval / (len(data) - minimizer.nfit), file=f)

        pars_fitted = Params.from_minuit(minimizer.params)
        print(pars_fitted, file=f)

    print(label)
    print("--------------------")
    print(pars_fitted.df)


def configs(filename="config/energies.json"):
    df = pd.read_json(filename)

    # Take only low energy
    df = df[df["energy"].str[0] < 100]

    # Consider only pp data
    df = df[df["process"] == "pp"]
    fields = df[["energy", "t", "filename", "process"]]
    return fields.to_dict(orient="records")


def main():
    for config in configs()[:1]:
        data = dataset(**config)
        pars = Params.from_dat()
        label = "{} {}".format(config["process"], config["energy"][0])

        m = fit(data, pars.values, ds)
        dump(data, m, label)

        plot(data, partial(ds, **m.values), label=label)


if __name__ == '__main__':
    main()

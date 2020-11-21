import sys
import iminuit

from toolz.functoolz import compose
from functools import partial
from iminuit.cost import LeastSquares

from extrapolate.vis import plot
from extrapolate.data import dataset
from extrapolate.params import Params
from extrapolate.observables import ds
from extrapolate.amplitudes import standard


def fit(data, pars, func):
    loss = LeastSquares(data["-t"], data["obs"], data["total err."], func)
    minimizer = iminuit.Minuit(loss, pedantic=True, **pars)
    minimizer.migrad(ncall=10000)
    return minimizer


def _dump(f, data, minimizer, label, outfile="output.dat"):
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


def dump(data, minimizer, label, outfile="output.dat"):
    pars_fitted = Params.from_minuit(minimizer.params)

    with open(outfile, "a") as f:
        _dump(f, data, minimizer, label)
        print(pars_fitted, file=f)

    _dump(sys.stdout, data, minimizer, label)
    print(pars_fitted.df)


def analyze(energy, t, process="pp",
            datafile="data/pp-bpp-data-v8.dat",
            paramsfile="config/params.dat"):
    data = dataset(energy, t, process, datafile)
    pars = Params.from_dat(filename=paramsfile)
    label = "{} {}".format(process, energy[0])

    m = fit(data, pars.values, compose(ds, standard))
    dump(data, m, label)

    plot(data, partial(standard, **m.values), label=label)
    return data, pars, m

import pytest
import pandas as pd

from toolz.functoolz import compose
from functools import partial
from iminuit.cost import LeastSquares

from extrapolate.amplitudes import standard
from extrapolate.params import Params
from extrapolate.analyze import analyze
from extrapolate.data import dataset
from extrapolate.vis import plot
from extrapolate.observables import ds


@pytest.fixture
def params():
    return "config/params.dat"


@pytest.fixture
def configs(filename="config/energies.json"):
    df = pd.read_json(filename)

    # Take only low energy
    df = df[df["energy"].str[0].between(62.3, 62.51)]

    # Consider only pp data
    df = df[df["process"] == "pp"]

    # Select only necessary fields
    fields = df[["energy", "t", "datafile", "process"]]
    return fields.to_dict(orient="records")


def test_debug(configs, params, datafile):
    for config in configs:
        analyze(**config)

        data = dataset(**config)

        pars = Params.from_dat(params)
        plot(data, partial(standard, **pars.values), label="no fit")
        func = compose(ds, partial(standard, **pars.values))
        loss = LeastSquares(data["-t"], data["obs"], data["total err."], func)
        print("Chi^2", loss())

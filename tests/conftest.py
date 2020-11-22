import pathlib

import pytest
import pandas as pd
import numpy as np

from extrapolate.data import DATAFIELDS
from extrapolate.amplitudes import standard
from extrapolate.observables import ds
from extrapolate.params import Params


def fake_datafile(path, t_range=(.5, 2.5), s=62.45, n_points=50):
    df = pd.DataFrame(0., index=np.arange(n_points), columns=DATAFIELDS)
    df["-t"] = np.linspace(*t_range, num=n_points)
    df["s"] = s
    df["code"] = 310
    df["obs"] = ds(standard(df["-t"], **Params.from_dat().values))
    df["total err."] = 0.01 * df["obs"]
    df.to_csv(path, index=False, sep="\t", header=None)
    return path


@pytest.fixture
def datafile():
    path = pathlib.Path("data/pp-bpp-data-v8.dat")

    # If the data folder exists then we are ready to go
    # NB: Don't add the data folder for version control
    if path.parent.exists():
        yield path
        return

    path.parent.mkdir()
    yield fake_datafile(path)
    path.unlink()
    path.parent.rmdir()

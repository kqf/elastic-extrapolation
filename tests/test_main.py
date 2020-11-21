import pytest
import pandas as pd
from extrapolate.analyze import analyze


@pytest.fixture
def configs(filename="config/energies.json"):
    df = pd.read_json(filename)

    # Take only low energy
    df = df[df["energy"].str[0] < 100]

    # Consider only pp data
    df = df[df["process"] == "pp"]

    # Select only necessary fields
    fields = df[["energy", "t", "datafile", "process"]]
    return fields.to_dict(orient="records")


@pytest.mark.onlylocal
def test_main(configs):
    for config in configs:
        analyze(**config)

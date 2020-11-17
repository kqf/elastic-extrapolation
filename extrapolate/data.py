import pandas as pd


DATAFIELDS = [
    "s", "-t", "obs", "stat", "syst", "total err.", "code"
]

OBS2CODE = {
    "pp": 310,
    "p#bar{p}": 311,
}


def dataset(energy, t, process="pp", filename="data/pp-bpp-data-v8.dat"):
    data = pd.read_csv(
        filename,
        sep=r"\s+",
        names=DATAFIELDS,
        usecols=[i for i, _ in enumerate(DATAFIELDS)]
    )
    # Ensure the right process
    data = data[data['code'] == OBS2CODE[process]]

    # Select the energy
    data = data[data['s'].between(*energy)]

    # Select the |t| interval
    data = data[data['-t'].between(*t)]
    return data.sort_values(["-t"])

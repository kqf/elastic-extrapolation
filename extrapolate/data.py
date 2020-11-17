import pandas as pd
from extrapolate.vis import vis


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
    return data


def main():
    data = dataset((13000, 13000))
    vis(data)


if __name__ == '__main__':
    main()

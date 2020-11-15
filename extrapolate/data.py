import numpy as np
import pandas as pd


FIELDS = [
    "s", "-t", "obs", "stat", "syst", "total err.", "code"
]

OBS2CODE = {
    "ds/dt pp": 310,
    "ds/dt p#bar{p}": 311,
}


def dataset(energy, process="ds/dt pp", filename="data/pp-bpp-data-v8.dat"):
    data = pd.read_csv(
        filename,
        sep=r"\s+",
        names=FIELDS,
        usecols=[i for i, _ in enumerate(FIELDS)]
    )
    data = data[data['code'] == OBS2CODE[process]]
    data = data[np.isclose(data['s'], energy)]
    data['-t'] = data['-t'].astype('float64')
    return data


def main():
    print(dataset(13000))


if __name__ == '__main__':
    main()

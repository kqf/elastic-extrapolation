import pandas as pd
import matplotlib.pyplot as plt


DATAFIELDS = [
    "s", "-t", "obs", "stat", "syst", "total err.", "code"
]

PARAMFIELDS = [
    "id", "name", "value", "err", "lower", "upper"
]


OBS2CODE = {
    "ds/dt pp": 310,
    "ds/dt p#bar{p}": 311,
}


def params(filename="data/params.dat"):
    df = pd.read_table(filename, sep=r"\s+", names=PARAMFIELDS)
    df["name"] = df["name"].str.replace("'", "")
    return df


def dataset(energy, process="ds/dt pp", filename="data/pp-bpp-data-v8.dat"):
    data = pd.read_csv(
        filename,
        sep=r"\s+",
        names=DATAFIELDS,
        usecols=[i for i, _ in enumerate(DATAFIELDS)]
    )
    data = data[data['code'] == OBS2CODE[process]]
    data = data[data['s'].between(*energy)]
    data['-t'] = data['-t'].astype('float64')
    return data


def main():
    data = dataset((13000, 13000))
    plt.errorbar(data["-t"], data["obs"],
                 yerr=data["total err."], fmt='.', markersize=0.1)
    plt.yscale("log")
    plt.xlabel("$|t|$ (GeV$^{2}$)")
    plt.ylabel(r"$d\sigma/dt$ (mb/GeV$^2$)")
    plt.show()


if __name__ == '__main__':
    main()

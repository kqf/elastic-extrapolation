import matplotlib.pyplot as plt
from contextlib import contextmanager


@contextmanager
def vis(data, func, label=None):
    f, (a0, a1) = plt.subplots(
        2, 1,
        gridspec_kw={'height_ratios': [3, 1]},
        sharex=True)

    a0.errorbar(data["-t"], data["obs"],
                yerr=data["total err."], fmt='.', markersize=0.1, label=label)
    # a0.yscale("log")

    a0.plot(data["-t"], func(data["-t"]), label="fit")

    a0.set_ylabel(r"$d\sigma/dt$ (mb/GeV$^2$)")
    a0.set_yscale('log')
    a0.legend()

    a1.plot(data["-t"], data["obs"] / func(data["-t"]), '.')
    a1.set_xlabel("$|t|$ (GeV$^{2}$)")
    a1.set_ylabel("$\\frac{\\rm{data}}{\\rm{fit}}$")

    yield plt
    plt.show()


def plot(data, func=None, label=None):
    with vis(data, func, label) as plt:
        plt.savefig(f"{label}.png")

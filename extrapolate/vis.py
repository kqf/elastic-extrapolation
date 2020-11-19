import matplotlib.pyplot as plt
from contextlib import contextmanager


@contextmanager
def vis(data, func=None, label=None):
    plt.errorbar(data["-t"], data["obs"],
                 yerr=data["total err."], fmt='.', markersize=0.1, label=label)
    if func is not None:
        plt.plot(data["-t"], func(data["-t"]), label="fit")

    plt.yscale("log")
    plt.xlabel("$|t|$ (GeV$^{2}$)")
    plt.ylabel(r"$d\sigma/dt$ (mb/GeV$^2$)")
    yield plt
    plt.show()


def plot(data, func=None, label=None):
    with vis(data, func, label) as plt:
        plt.legend()
        plt.savefig(f"{label}.png")

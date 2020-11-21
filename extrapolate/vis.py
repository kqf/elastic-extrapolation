import matplotlib.pyplot as plt
from contextlib import contextmanager


@contextmanager
def vis(data, func, label=None):
    a1 = plt.subplot2grid((4, 2), (0, 0), rowspan=3)
    a2 = plt.subplot2grid((4, 2), (3, 0), sharex=a1)
    a4 = plt.subplot2grid((4, 2), (0, 1), rowspan=4)

    # Plot the data and the fitted function
    a1.errorbar(data["-t"], data["obs"],
                yerr=data["total err."], fmt='.', markersize=0.1, label=label)
    a1.plot(data["-t"], func(data["-t"]), label="fit")
    a1.set_ylabel(r"$d\sigma/dt$ (mb/GeV$^2$)")
    a1.set_yscale('log')
    a1.legend()

    # Plot the ratio
    a2.plot(data["-t"], data["obs"] / func(data["-t"]), '.')
    a2.plot(data["-t"], data["-t"] * 0. + 1., 'k--')
    a2.set_xlabel("$|t|$ (GeV$^{2}$)")
    a2.set_ylabel("$\\frac{\\rm{data}}{\\rm{fit}}$")

    # Plot the real to imaginary ratio
    a4.errorbar(data["-t"], func(data["-t"]), label="fit")
    a4.set_ylabel(r"$\rho(t)$")
    a4.set_xlabel("$|t|$ (GeV$^{2}$)")

    plt.tight_layout()
    plt.subplots_adjust(hspace=0)

    yield plt
    plt.show()


def plot(data, func=None, label=None):
    with vis(data, func, label) as plt:
        plt.savefig(f"{label}.png")

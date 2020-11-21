import matplotlib.pyplot as plt

from contextlib import contextmanager
from extrapolate.observables import ds, rho


@contextmanager
def vis(data, func, label=None):
    # Configure plotting
    a1 = plt.subplot2grid((4, 2), (0, 0), rowspan=3)
    a2 = plt.subplot2grid((4, 2), (3, 0), sharex=a1)
    a4 = plt.subplot2grid((4, 2), (0, 1), rowspan=4)
    errorbar_cfg = dict(
        ls='',
        marker='o',
        markersize=2,
        # markerfacecolor='none',
        capsize=1,
        capthick=1,
        # ecolor='black'
    )

    t, y, dy = data["-t"], data["obs"], data["total err."]
    amplitude = func(t)
    yhat = ds(amplitude)

    # Plot the data and the fitted function
    a1.errorbar(t, y, yerr=dy, label=label, **errorbar_cfg)

    a1.plot(t, yhat, label="fit")
    a1.set_ylabel(r"$d\sigma/dt$ (mb/GeV$^2$)")
    a1.set_yscale('log')
    a1.legend()

    # Plot the ratio
    a2.errorbar(t, y / yhat, yerr=dy / yhat, **errorbar_cfg)
    a2.plot(t, t * 0. + 1., 'k--')
    a2.set_xlabel("$|t|$ (GeV$^{2}$)")
    a2.set_ylabel("$\\frac{\\rm{data}}{\\rm{fit}}$")

    # Plot the real to imaginary ratio
    a4.errorbar(t, rho(amplitude), label="fit")
    a4.set_ylabel(r"$\rho(t)$")
    a4.set_xlabel("$|t|$ (GeV$^{2}$)")

    plt.tight_layout()
    plt.subplots_adjust(hspace=0)

    yield plt
    plt.show()


def plot(data, func=None, label=None):
    with vis(data, func, label) as plt:
        plt.savefig(f"{label}.png")

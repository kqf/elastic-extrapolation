import pandas as pd

from contextlib import contextmanager
from operator import attrgetter


@contextmanager
def custom_format(custom):
    standard = pd.get_option('display.float_format')
    pd.set_option('display.float_format', custom)
    yield
    pd.set_option('display.float_format', standard)


def scientific(x, pattern="{:.5E}"):
    return pattern.format(x)


class Params:
    fields = ["number", "name", "value", "error", "lower_limit", "upper_limit"]

    def __init__(self, df):
        self.df = df.set_index("name")

    @property
    def limits(self):
        limits = self.df[["lower_limit", "upper_limit"]].copy()
        limits.index = "limit_" + limits.index
        limits["limit"] = limits.apply(tuple, axis=1)
        return limits["limit"].to_dict()

    @property
    def values(self):
        return self.df["value"].to_dict()

    def to_minuit(self, limits=True):
        output = {}
        output.update(self.values)
        if limits:
            output.update(self.limits)
        return output

    @classmethod
    def from_minuit(cls, params):
        df = pd.DataFrame({"raw": params})
        for field in cls.fields:
            df[field] = df["raw"].apply(attrgetter(field))

        # Fortran indexing
        return cls(df.drop(columns=["raw"]))

    @classmethod
    def from_dat(cls, filename="config/params.dat", dropna=True):
        df = pd.read_table(filename, sep=r"\s+", names=cls.fields)
        if dropna:
            df = df.dropna()
        df["name"] = df["name"].str.replace("'", "")
        return cls(df)

    def __repr__(self):
        with custom_format(scientific):
            return str(self.df)

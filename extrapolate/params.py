import pandas as pd


class Params:
    fields = ["id", "name", "value", "err", "lower", "upper"]

    def __init__(self, filename="data/params.dat", dropna=True):
        df = pd.read_table(filename, sep=r"\s+", names=self.fields)
        if dropna:
            df = df.dropna()
        df["name"] = df["name"].str.replace("'", "")
        self.df = df.set_index("name")

    @property
    def limits(self):
        limits = self.df[["lower", "upper"]]
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

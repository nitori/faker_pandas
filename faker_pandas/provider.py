from faker.providers import BaseProvider
from faker.generator import random
from functools import partial
import pandas as pd

_AUTO = object()


class PandasProvider(BaseProvider):

    def pandas_dataframe(
        self,
        *generators,
        columns=None,
        rows=7,
        index=_AUTO
    ):

        if index is _AUTO:
            index = range(1, rows + 1)

        row_list = []
        for _ in range(rows):
            row = []
            for generator in generators:
                row.append(generator())
            row_list.append(row)

        if columns is None:
            columns = []
            for generator in generators:
                columns.append(generator.__name__)
        else:
            columns = list(columns)[:len(generators)]
            for generator in generators[len(columns):]:
                columns.append(generator.__name__)

        df = pd.DataFrame(row_list, index=index, columns=columns)
        return df

    def pandas_series_generator(self):
        return SeriesGenerator(self.generator)


class SeriesGenerator:
    def __init__(self, generator):
        self.generator = generator

    def __getattr__(self, item):
        func = getattr(self.generator, item)

        def _gen(name):
            return _SeriesCaller(name, func)

        return _gen

    def pandas_int(self, name, a, b, *, nan_ratio=0):
        def _gen():
            return random.choices(
                [random.randint(a, b), float('nan')],
                [1 - nan_ratio, nan_ratio],
                k=1
            )[0]

        return _SeriesCaller(name, _gen)

    def pandas_float(self, name, *, nan_ratio=0):
        def _gen():
            return random.choices(
                [random.random(), float('nan')],
                [1 - nan_ratio, nan_ratio],
                k=1
            )[0]

        return _SeriesCaller(name, _gen)


class _SeriesCaller:

    def __init__(self, name, func, *args, **kwargs):
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    @property
    def __name__(self):
        return self.name

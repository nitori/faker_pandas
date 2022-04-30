from faker.providers import BaseProvider
from faker.generator import random
from functools import partial, wraps
import pandas as pd

_AUTO = object()


class PandasProvider(BaseProvider):

    def pandas_dataframe(
        self,
        *generators,
        rows=7,
        index=_AUTO
    ):
        if index is _AUTO:
            index = range(1, rows + 1)

        row_list = []
        for _ in range(rows):
            row = []
            for generator in generators:
                row.append(next(generator))
            row_list.append(row)

        columns = []
        for generator in generators:
            columns.append(generator.__name__)

        df = pd.DataFrame(row_list, index=index, columns=columns)
        return df

    def pandas_column_generator(self):
        return ColumnGenerator(self.generator)


def argumentarize(func):
    @wraps(func)
    def decorator(decorated_func=None, /, **kwargs):
        if decorated_func is None:
            # decorator was used with (...)
            # so return the decorator again as partial
            return partial(func, **kwargs)
        if not callable(decorated_func):
            raise TypeError(f"First argument of {func} must be callable. Use keyword arguments instead.")
        return func(decorated_func, **kwargs)

    return decorator


@argumentarize
def wrap_iterator(func, /, **deco_kwargs):
    @wraps(func)
    def _wrapper(self, name, *args, **kwargs):
        if not hasattr(func, '__self__'):
            bound_func = func.__get__(self, self.__class__)
        else:
            bound_func = func

        passed_kwargs = {**deco_kwargs, **kwargs}
        return ColumnIterator(name, bound_func, *args, **passed_kwargs)

    return _wrapper


class ColumnGenerator:
    def __init__(self, generator):
        self.generator = generator

    def __getattr__(self, item):
        func = getattr(self.generator, item)
        return partial(wrap_iterator(func), self.generator)

    @wrap_iterator(empty_value=float('nan'))
    def pandas_int(self, a, b):
        return random.randint(a, b)

    @wrap_iterator(empty_value=float('nan'))
    def pandas_float(self):
        return random.random(0, 1)


class ColumnIterator:

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        if 'rows' in kwargs:
            obj.__init__(*args, **kwargs)
            return obj.to_series()
        return obj

    def __init__(self, name, func, *args, rows=None, empty_value=None, empty_ratio=0.0, **kwargs):
        self.name = name
        self.func = func
        self.args = args
        self.kwargs = kwargs

        self.rows = rows
        self.empty_value = empty_value
        self.empty_ratio = empty_ratio

    @property
    def __name__(self):
        return self.name

    def __iter__(self):
        return self

    def __next__(self):
        if random.random() < self.empty_ratio:
            return self.empty_value
        return self.func(*self.args, **self.kwargs)

    def to_series(self, *, rows=None):
        if rows is None:
            rows = self.rows
        if rows is None:
            raise ValueError('rows is not specified')
        return pd.Series(item for item, _ in zip(self, range(rows)))

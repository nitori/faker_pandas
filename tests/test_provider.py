import pytest
from faker import Faker
from faker_pandas import PandasProvider, ColumnGenerator, ColumnIterator
import pandas


@pytest.fixture(scope="session")
def fake():
    fake = Faker()
    fake.add_provider(PandasProvider)
    return fake


@pytest.fixture(scope="session")
def colgen(fake) -> ColumnGenerator:
    return fake.pandas_column_generator()


def test_iterator_return(fake, colgen):
    series = colgen.pandas_int('Age', 10, 20)
    assert isinstance(series, ColumnIterator)


def test_series_return(fake, colgen):
    series = colgen.pandas_int('Age', 10, 20, rows=3)
    assert isinstance(series, pandas.Series)
    assert len(series) == 3

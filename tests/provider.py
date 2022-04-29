import pytest
from faker import Faker
from faker_pandas import PandasProvider


@pytest.fixture(scope="session")
def fake():
    fake = Faker()
    fake.add_provider(PandasProvider)
    return fake


def test_provider(fake):
    assert True


# Faker Pandas

```py
from faker import Faker
from faker_pandas import PandasProvider

fake = Faker()
fake.add_provider(PandasProvider)

series = fake.pandas_series_generator()

df = fake.pandas_dataframe(
    series.first_name('First Name'),
    series.last_name('Last Name'),
    series.pandas_int('Age', 18, 80),
    rows=5
)

print(df)
```
Output:
```txt
  First Name Last Name  Age
1   Kimberly  Humphrey   63
2     Leslie     White   55
3    Melanie     Brown   20
4   Jennifer      Diaz   23
5      Eddie     Ellis   63
```

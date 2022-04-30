
# Faker Pandas

```py
from faker import Faker
from faker_pandas import PandasProvider

fake = Faker()
fake.add_provider(PandasProvider)

colgen = fake.pandas_column_generator()

df = fake.pandas_dataframe(
    colgen.first_name('First Name', empty_value='', empty_ratio=.5),
    colgen.last_name('Last Name'),
    colgen.pandas_int('Age', 18, 80, empty_ratio=.2),
    rows=7
)

print(df)
```
Output:
```txt
  First Name Last Name   Age
1             Lawrence  72.0
2       Lisa  Holloway   NaN
3              Edwards  31.0
4     Steven   Johnson  69.0
5                Smith  66.0
6     Monica     Lynch   NaN
7     Edward     Brown  20.0
```

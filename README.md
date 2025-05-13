# pandas_col

Sick of doing

```python
df.assign(c = lambda df: df['a'] + df['b'])
```
in pandas?

Do
```python
from pandas_col import col

df.assign(c = col('a') + col('b'))
```
instead!

## Installation

For now, just clone this repo and import `pandas_col`.

I can publish it to PyPI if anyone would actually want to use this.

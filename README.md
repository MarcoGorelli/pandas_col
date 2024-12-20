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

```
pip install git+https://github.com/MarcoGorelli/pandas_col.git
```
I can publish it to PyPI if anyone would actually want to use this.


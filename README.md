# pandas_col

Sick of doing

```python
df.assign(**{col: lambda df: df[col] + 10 for col in ("a", "b")}))
```
in pandas and having it not do what you expect?

Do
```python
from pandas_col import col

df.assign(**{col: col(col) + 10 for col in ("a", "b")})
```
instead!

## Is this project serious?

idk. I'm just publishing it cause it's possible. Curious what
people think about it.


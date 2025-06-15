from __future__ import annotations
import pandas as pd

from pandas_col import col
from datetime import datetime


df = pd.DataFrame(
    {
        "a": [1, 2, 3],
        "b": [4, 5, 619],
        "c": [datetime(2020, 1, 1), datetime(2020, 1, 2), datetime(2020, 1, 3)],
    }
)
print(df.assign(**{x: lambda df: df[x] + 10 for x in ("a", "b")}))
print(df.assign(**{x: col(x) + 10 for x in ("a", "b")}))
print(df.assign(**{x: 10+col(x) for x in ("a", "b")}))

print(df.assign(c=col("a").shift(1)))
print(
    df.assign(
        x = 1+col('a'),
        y = 1-col('a'),
        c_formatted=col("c").dt.strftime("%Y/%m/%d"),
        b_other=col("b").astype(str).str.len(),
    )
)

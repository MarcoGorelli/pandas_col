import pandas as pd

import pandas_col
from datetime import datetime

pd.col = pandas_col.col


import pandas as pd

df = pd.DataFrame(
    {
        "a": [1, 2, 3],
        "b": [4, 5, 619],
        "c": [datetime(2020, 1, 1), datetime(2020, 1, 2), datetime(2020, 1, 3)],
    }
)
print(df.assign(**{col: lambda df: df[col] + 10 for col in ("a", "b")}))
print(df.assign(**{col: pd.col(col) + 10 for col in ("a", "b")}))
print(df.assign(**{col: 10+pd.col(col) for col in ("a", "b")}))

print(df.assign(c=pd.col("a").shift(1)))
print(
    df.assign(
        x = 1+pd.col('a'),
        y = 1-pd.col('a'),
        c_formatted=pd.col("c").dt.strftime("%Y/%m/%d"),
        b_other=pd.col("b").astype(str).str.len(),
    )
)

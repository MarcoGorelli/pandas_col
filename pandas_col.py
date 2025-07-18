from __future__ import annotations
from typing import Hashable, TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from pandas import DataFrame, Series


def parse_args(df: DataFrame, *args):
    return tuple([x(df) if isinstance(x, Expr) else x for x in args])


def parse_kwargs(df: DataFrame, **kwargs):
    return {
        key: val(df) if isinstance(val, Expr) else val for key, val in kwargs.items()
    }


class Expr:
    def __init__(self, func: Callable[[DataFrame], Series]):
        self._func = func

    def __call__(self, df: DataFrame) -> Series:
        return self._func(df)

    # namespaces
    @property
    def dt(self):
        return NamespaceExpr(self, "dt")

    @property
    def str(self):
        return NamespaceExpr(self, "str")

    @property
    def cat(self):
        return NamespaceExpr(self, "cat")

    @property
    def list(self):
        return NamespaceExpr(self, "list")

    @property
    def sparse(self):
        return NamespaceExpr(self, "sparse")

    @property
    def struct(self):
        return NamespaceExpr(self, "struct")

    # Binary ops

    def __add__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__add__(other(df)))
        return Expr(lambda df: self(df).__add__(other))

    def __radd__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__radd__(other(df)))
        return Expr(lambda df: self(df).__radd__(other))

    def __sub__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__sub__(other(df)))
        return Expr(lambda df: self(df).__sub__(other))

    def __rsub__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__rsub__(other(df)))
        return Expr(lambda df: self(df).__rsub__(other))

    def __mul__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__mul__(other(df)))
        return Expr(lambda df: self(df).__mul__(other))

    def __rmul__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__rmul__(other(df)))
        return Expr(lambda df: self(df).__rmul__(other))

    def __truediv__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__truediv__(other(df)))
        return Expr(lambda df: self(df).__truediv__(other))

    def __rtruediv__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__rtruediv__(other(df)))
        return Expr(lambda df: self(df).__rtruediv__(other))

    def __floordiv__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__floordiv__(other(df)))
        return Expr(lambda df: self(df).__floordiv__(other))

    def __rfloordiv__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__rfloordiv__(other(df)))
        return Expr(lambda df: self(df).__rfloordiv__(other))

    def __ge__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__ge__(other(df)))
        return Expr(lambda df: self(df).__ge__(other))

    def __gt__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__gt__(other(df)))
        return Expr(lambda df: self(df).__gt__(other))

    def __le__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__le__(other(df)))
        return Expr(lambda df: self(df).__le__(other))

    def __lt__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__lt__(other(df)))
        return Expr(lambda df: self(df).__lt__(other))

    def __eq__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__eq__(other(df)))
        return Expr(lambda df: self(df).__eq__(other))

    def __neq__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__neq__(other(df)))
        return Expr(lambda df: self(df).__neq__(other))

    def __mod__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__mod__(other(df)))
        return Expr(lambda df: self(df).__mod__(other))

    # Everything else

    def __getattr__(self, attr):
        def func(df, *args, **kwargs):
            args = parse_args(df, *args)
            kwargs = parse_kwargs(df, **kwargs)
            return getattr(self(df), attr)(*args, **kwargs)

        return lambda *args, **kwargs: Expr(lambda df: func(df, *args, **kwargs))


class NamespaceExpr:
    def __init__(self, func: Callable[[DataFrame], Series], namespace: str) -> None:
        self._func = func
        self._namespace = namespace

    def __getattr__(self, attr: str) -> Any:
        def func(df, *args, **kwargs):
            args = parse_args(df, *args)
            kwargs = parse_kwargs(df, **kwargs)
            return getattr(getattr(self._func(df), self._namespace), attr)(
                *args, **kwargs
            )

        return lambda *args, **kwargs: Expr(lambda df: func(df, *args, **kwargs))


def col(col_name: Hashable) -> Expr: 
    if not isinstance(col_name, Hashable):
        msg = f"Expected Hashable, got: {type(col_name)}"
        raise TypeError(msg)
    return Expr(lambda df: df[col_name])


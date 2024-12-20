from typing import Hashable

def parse_args(df, *args):
    return tuple([x(df) if isinstance(x, Expr) else x for x in args])


def parse_kwargs(df, **kwargs):
    return {
        key: val(df) if isinstance(val, Expr) else val for key, val in kwargs.items()
    }


class Expr:
    def __init__(self, func):
        self._func = func

    def __call__(self, df):
        return self._func(df)

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

    def __prod__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__prod__(other(df)))
        return Expr(lambda df: self(df).__prod__(other))

    def __truediv__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__truediv__(other(df)))
        return Expr(lambda df: self(df).__truediv__(other))

    def __floordiv__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__floordiv__(other(df)))
        return Expr(lambda df: self(df).__floordiv__(other))

    def __mod__(self, other):
        if isinstance(other, Expr):
            return Expr(lambda df: self(df).__mod__(other(df)))
        return Expr(lambda df: self(df).__mod__(other))

    def __getattr__(self, attr):
        def func(df, *args, **kwargs):
            args = parse_args(df, *args)
            kwargs = parse_kwargs(df, **kwargs)
            return getattr(self(df), attr)(*args, **kwargs)

        return lambda *args, **kwargs: Expr(lambda df: func(df, *args, **kwargs))

    @property
    def dt(self):
        return DateTimeExpr(self)

    @property
    def str(self):
        return StringExpr(self)

    @property
    def cat(self):
        return CatExpr(self)


class DateTimeExpr:
    def __init__(self, func):
        self._func = func

    def __getattr__(self, attr):
        def func(df, *args, **kwargs):
            args = parse_args(df, *args)
            kwargs = parse_kwargs(df, **kwargs)
            return getattr(self._func(df).dt, attr)(*args, **kwargs)

        return lambda *args, **kwargs: Expr(lambda df: func(df, *args, **kwargs))


class StringExpr:
    def __init__(self, func):
        self._func = func

    def __getattr__(self, attr):
        def func(df, *args, **kwargs):
            args = parse_args(df, *args)
            kwargs = parse_kwargs(df, **kwargs)
            return getattr(self._func(df).str, attr)(*args, **kwargs)

        return lambda *args, **kwargs: Expr(lambda df: func(df, *args, **kwargs))


class CatExpr:
    def __init__(self, func):
        self._func = func

    def __getattr__(self, attr):
        def func(df, *args, **kwargs):
            args = parse_args(df, *args)
            kwargs = parse_kwargs(df, **kwargs)
            return getattr(self._func(df).cat, attr)(*args, **kwargs)

        return lambda *args, **kwargs: Expr(lambda df: func(df, *args, **kwargs))


def col(col_name):
    if not isinstance(col_name, Hashable):
        msg = f"Expected Hashable, got: {type(col_name)}"
        raise TypeError(msg)
    return Expr(lambda df: df[col_name])

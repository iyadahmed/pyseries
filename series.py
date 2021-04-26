from abc import ABC, abstractmethod
from typing import Union, Iterable, SupportsInt
from operator import add, pow


# TODO: Implement Finite and InfiniteSeries


class Series(ABC):
    def __repr__(self) -> str:
        name = self.__class__.__name__.strip("Series")
        return "{}: ({}, {}, {}, ...)".format(name, *self[0:3])  # type: ignore

    def __add__(self, other):
        if type(other) in (float, int):
            return BinaryOpSeries(self, FixedSeries(other), add)
        return BinaryOpSeries(self, other, add)

    def __pow__(self, other):
        if type(other) in (float, int):
            return BinaryOpSeries(self, FixedSeries(other), pow)
        return BinaryOpSeries(self, other, pow)

    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.stop is None:
                raise KeyError("Series slice must specify stop")
            return tuple(self.__getith__(i) for i in range(key.start or 0, key.stop, key.step or 1))

        if isinstance(key, int):
            return self.__getith__(key)

        t = key.__class__.__name__
        raise TypeError(f"Series indices must be integers or slices, not {t}")

    @abstractmethod
    def __getith__(self, key: int):
        pass


class BinaryOpSeries(Series):
    """ Element-wise binary operation on two series """

    def __init__(self, s1, s2, op):
        self.s1 = s1
        self.s2 = s2
        self.op = op

    def __getith__(self, i):
        return self.op(self.s1[i], self.s2[i])


class UniaryOpSeries(Series):
    def __init__(self, s, op):
        self.s = s
        self.op = op

    def __getith__(self, i):
        return self.op(self.s[i])


class DiffSeries(Series):
    def __init__(self, s):
        self.s = s

    def __getith__(self, i):
        return self.s[i + 1] - self.s[i]


class AccumSeries(Series):
    def __init__(self, s):
        self.s = s

    def __getith__(self, i):
        return sum(self.s[0:i+1])


class FixedSeries(Series):
    def __init__(self, value):
        self.value = value

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __getith__(self, i):
        return self.value


class ArithmeticSeries(Series):
    def __init__(self, a, d):
        self._a = a
        self._d = d

    def __add__(self, other):
        if isinstance(other, ArithmeticSeries):
            return ArithmeticSeries(self._a + other._a, self._d + other._d)
        return Series.__add__(self, other)

    def __eq__(self, other):
        return (self._a == other._a) and (self._d == other._d)

    def __getith__(self, i):
        return self._a + i * self._d

    @staticmethod
    def from_series(s):
        """ Try to build an arthimetic series from a series of numbers
        >>> ArithmeticSeries.from_series([3, 9, 15, 21]) == ArithmeticSeries(3, 6)
        True
        """
        isconst = True
        prev_d = None
        for i in range(len(s) - 1):
            d = s[i + 1] - s[i]
            if prev_d is not None:
                if (d != prev_d):
                    isconst = False
                    break
            prev_d = d

        if not isconst:
            raise ValueError(
                "Iterable values don't have a constant difference")

        return ArithmeticSeries(s[0], d)


class GeometricSeries(Series):
    """
    >>> GeometricSeries(3, 2)
    Geometric: (3, 6, 12, ...)
    >>> GeometricSeries(4, 3)[:]
    Traceback (most recent call last):
        ...
    KeyError: 'Series slice must specify stop'
    >>> sum(GeometricSeries(2, .5)[:100])
    4.0
    """

    def __init__(self, a, r):
        self._a = a
        self._r = r

    def __eq__(self, other):
        return (self._a == other._a) and (self._r == other._r)

    def __getith__(self, i):
        a = self._a
        r = self._r
        return a * (r ** i)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    a = GeometricSeries(1, 2)
    b = ArithmeticSeries(1, 2)
    c = a + b
    print(sum((b ** -100)[:10000]))
    print(AccumSeries(c) + DiffSeries(c))

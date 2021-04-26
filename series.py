from abc import ABC, abstractmethod
from typing import Union, Iterable, SupportsInt

# TODO: Implement GenericSeries
# TODO: Implement Finite and InfiniteSeries


class Series(ABC):
    def __repr__(self) -> str:
        # TODO: don't display dots for convergent series
        # TODO: display type of series
        return "{}, {}, {}, ...".format(*self[0:3])

    def __getitem__(self, key: Union[int, slice]) -> None:
        if isinstance(key, slice):
            if key.stop is None:
                raise KeyError("Series slice must specify stop")
            return self.__slice__(key)

        if isinstance(key, int):
            return self.__getith__(key)

        t = key.__class__.__name__
        raise TypeError(f"Series indices must be integers or slices, not {t}")

    @abstractmethod
    def __slice__(self, key: slice) -> Iterable:
        pass

    @abstractmethod
    def __getith__(self, key: int) -> SupportsInt:
        pass


class ArithmeticSeries(Series):
    def __init__(self, a: SupportsInt, d: SupportsInt) -> None:
        self._a = a
        self._d = d

    def __add__(self, other: "ArithmeticSeries") -> "ArithmeticSeries":
        # TODO: support adding numbers
        return ArithmeticSeries(self._a + other._a, self._d + other._d)

    def __eq__(self, other: "ArithmeticSeries") -> bool:
        return (self._a == other._a) and (self._d == other._d)

    def __slice__(self, s: slice) -> Iterable:
        a = self._a
        d = self._d
        return range(a + s.start * d, a + s.stop * d, d)

    def __getith__(self, i: int) -> SupportsInt:
        return self._a + i * self._d

    @staticmethod
    def from_iterable(s: Iterable[SupportsInt], a=None) -> "ArithmeticSeries":
        """ Try to build an arthimetic series from an iterable of numbers
        >>> ArithmeticSeries.from_iterable([3, 9, 15, 21]) == ArithmeticSeries(3, 6)
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

        return ArithmeticSeries(a or s[0], d)


class GeometricSeries(Series):
    """
    >>> GeometricSeries(3, 2)
    3, 6, 12, ...
    >>> GeometricSeries(4, 3)[:]
    Traceback (most recent call last):
        ...
    KeyError: 'Series slice must specify stop'
    >>> sum(GeometricSeries(2, .5)[:100])
    4.0
    """

    def __init__(self, a: SupportsInt, r: SupportsInt) -> None:
        self._a = a
        self._r = r

    def __slice__(self, s: slice) -> Iterable:
        a = self._a
        r = self._r
        return (a * (r ** i) for i in range(s.start or 0, s.stop, s.step or 1))

    def __getith__(self, i: int) -> SupportsInt:
        a = self._a
        r = self._r
        return a * (r ** i)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

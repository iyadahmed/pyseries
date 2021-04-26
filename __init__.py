from abc import ABC, abstractmethod
from typing import Union, Iterable, SupportsInt


class Series(ABC):
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


class ArthimeticSeries(Series):
    def __init__(self, a: SupportsInt, d: SupportsInt) -> None:
        self._a = a
        self._d = d

    def __slice__(self, key: slice) -> Iterable:
        a = self._a
        d = self._d
        return range(a + key.start * d, a + key.stop * d, d)

    def __getith__(self, i):
        return self._a + i * self._d
    



    # def __getitem__(self, key):
    #     if isinstance(key, slice):
    #         if key.stop is None:
    #             raise KeyError("Series slice must specify stop")
    #         a = self._a
    #         d = self._d
    #         return range(a + key.start * d, a + key.stop * d, d)
    #     if isinstance(key, int):
    #         return self._a + key * self._d
    #     t = key.__class__.__name__
    #     raise TypeError(f"Series indices must be integers or slices, not {t}")


# class GeometricSeries:
#     def __init__(self, a, r):
#         self._a = a
#         self._r = r

#     def __getitem__(self, key)


foo = ArthimeticSeries(0, 5)
for i in foo[20:0]:
    print(i)

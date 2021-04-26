class ArthimeticSeries:
    def __init__(self, a, d):
        self._a = a
        self._d = d
        self._func = lambda i: a + i * d

    def __getitem__(self, s):
        if isinstance(s, slice):
            return (self._func(i) for i in range(s.start, s.stop, s.step or 1))



foo = ArthimeticSeries(0, 1)
print(foo[0:1]
##for i in foo[0:1]:
##    print(i)

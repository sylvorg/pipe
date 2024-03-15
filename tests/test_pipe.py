from functools import partial
from pipe import Pipe, pipe
from string import ascii_lowercase as lower
from pytest import fixture, mark


@mark.pipe
class TestPipe:
    @fixture
    def a(self, scope="class"):
        return 5

    @fixture
    def b(self, scope="class"):
        return 5

    @fixture
    def tenc(self, a, b, scope="class"):
        return [str(i) for i in range(a + b)]

    @fixture
    def f1(self, scope="class"):
        return partial(map, str)

    @fixture
    def f2(self, scope="class"):
        return list

    @fixture
    def f10(self):
        return Pipe(lambda *args, **kwargs: range(sum(args) + sum(kwargs.values())))

    def test_decorator(self):
        @Pipe
        def f10(*args, **kwargs):
            return range(sum(args) + sum(kwargs.values()))

        assert isinstance(f10, Pipe)

    def test_pipe(self, a, b, tenc, f1, f2, f10):
        assert (f10 | f1 | f2)(a, b=b) == tenc

    def test_rshift(self, a, b, tenc, f1, f2, f10):
        assert (f10 >> f1 >> f2)(a, b=b) == tenc

    def test_lshift(self, a, b, tenc, f1, f2, f10):
        assert (Pipe(f2) << f1 << f10)(a, b=b) == tenc

    # TODO: All possible combinations?
    # f10 >> f1 << f2
    # f10 << f1 >> f2
    # Or similar


@mark.pipe
@mark.usefixtures("a", "b", "tenc", "f1", "f2", "f10")
class TestInPlacePipe(TestPipe):
    def test_pipe(self, a, b, tenc, f1, f2, f10):
        f10 |= f1
        f10 |= f2
        assert f10(a, b=b) == tenc

    def test_rshift(self, a, b, tenc, f1, f2, f10):
        f10 >>= f1
        f10 >>= f2
        assert f10(a, b=b) == tenc

    def test_lshift(self, a, b, tenc, f1, f2, f10):
        f2 = Pipe(f2)
        f2 <<= f1
        f2 <<= f10
        assert f2(a, b=b) == tenc


@mark.pipe
@mark.usefixtures("a", "b", "tenc", "f1", "f2")
class TestPiping(TestPipe):
    @fixture
    def funcs(self, scope="class"):
        funcs = []
        for c in lower:

            def f(a, b=0, c=c):
                aString = isinstance(a, str)
                return (
                    f"{(int(a[0]) if aString else a) + b}{a[1:] if aString else ''}{c}"
                )

            funcs.append(f)
        return funcs

    # Adapted From:
    # Answer: https://stackoverflow.com/a/7546960/10827766
    # User: https://stackoverflow.com/users/247357/snakehiss
    def test_reducer(self, a, b, funcs):
        assert pipe(funcs)(a) == (str(a) + lower)
        assert pipe(funcs)(a, b=b) == (str(a + b) + lower)

    def test_wrap(self, a, b, tenc, f1, f2):
        @Pipe.wrap(f2)
        @Pipe.wrap(f1)
        def f10(*args, **kwargs):
            return range(sum(args) + sum(kwargs.values()))

        assert f10(a, b=b) == tenc

import operator
from collections.abc import Callable
from functools import wraps, reduce
from more_itertools import collapse
from typing import Any, Unpack


def flatten(*args):
    return list(collapse(args))


class PipeMeta(type):
    # wrap = lambda cls, b: lambda a: lambda *args, **kwargs: b(a(*args, **kwargs))
    def wrap(cls: "PipeMeta", b: Callable) -> Callable:
        def wrapper(a: Callable):
            @wraps(a)
            def wrapped(*args: Unpack[Any], **kwargs: Unpack[Any]):
                return b(a(*args, **kwargs))

            return wrapped

        return wrapper


class Pipe(metaclass=PipeMeta):
    def __init__(self: "Pipe", func: Callable) -> None:
        self.func: Callable = func.func if isinstance(func, self.__class__) else func

    def __wrap__(self: "Pipe", b: Callable, a: Callable) -> Callable:
        return self.__class__.wrap(b)(a)

    def __call__(self: "Pipe", *args: Unpack[Any], **kwargs: Unpack[Any]) -> Any:
        return self.func(*args, **kwargs)

    def __or__(self: "Pipe", other: Callable) -> "Pipe":
        return self.__class__(self.__wrap__(other, self.func))

    def __rshift__(self: "Pipe", other: Callable) -> "Pipe":
        return self.__or__(other)

    def __rlshift__(self: "Pipe", other: Callable) -> "Pipe":
        return self.__or__(other)

    def __ror__(self: "Pipe", other: Callable) -> "Pipe":
        return self.__class__(self.__wrap__(self.func, other))

    def __rrshift__(self: "Pipe", other: Callable) -> "Pipe":
        return self.__ror__(other)

    def __lshift__(self: "Pipe", other: Callable) -> "Pipe":
        return self.__ror__(other)

    def __ior__(self: "Pipe", other: Callable) -> "Pipe":
        self.func = self.__wrap__(other, self.func)
        return self

    def __irshift__(self: "Pipe", other: Callable) -> "Pipe":
        return self.__ior__(other)

    def __ilshift__(self: "Pipe", other: Callable) -> "Pipe":
        self.func = self.__wrap__(self.func, other)
        return self


def pipe(*funcs: Unpack[Callable]) -> Pipe:
    funcs: list[Callable] = flatten(funcs)
    if funcs:
        init: Pipe = Pipe(funcs[0])
        if len(funcs) > 1:
            return reduce(
                operator.ior,
                funcs[1:],
                init,
            )
            # return reduce(
            #     lambda a, b: Pipe.wrap(b)(a),
            #     lambda a, b: lambda *args, **kwargs: b(a(*args, **kwargs)),
            #     funcs,
            # )
        return init
    return Pipe(lambda x: x)

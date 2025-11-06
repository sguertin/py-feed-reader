from typing import TypeVar


T = TypeVar("T")


def first(iter: list[T], default: T | None = None) -> T | None:
    if not iter:
        return default
    return iter[0]

from __future__ import annotations

import functools
import sys
import uuid
from typing import Any, Callable, Hashable, NamedTuple, TypeVar

import streamlit as st

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

CACHE_KEY_PREFIX = (
    uuid.uuid4().hex
)  # To make the key more unique even when args or kwargs are so simple


def get_fully_qualified_name(func: Callable[..., Any]) -> str:
    module_name = func.__module__
    qualname = func.__qualname__
    return f"{module_name}.{qualname}"


def calc_cache_key(
    func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any]
) -> str:
    hashable_args = [a if isinstance(a, Hashable) else id(a) for a in args]
    hashable_kwargs = {
        k: v if isinstance(v, Hashable) else id(v) for k, v in kwargs.items()
    }
    # `st.session_state` accepts `str` and `int` keys and stringifies whatever it
    # is given, so the tuple is stringified here rather than relying on that.
    return str(
        (
            CACHE_KEY_PREFIX,
            get_fully_qualified_name(func),
            tuple(hashable_args),
            tuple(sorted(hashable_kwargs.items())),
        )
    )


class CacheEntry(NamedTuple):
    value: Any
    # The arguments are kept alive by the entry that they are keyed by:
    # `calc_cache_key()` falls back to `id()` for unhashable arguments, and CPython
    # reuses the address of a freed object, so releasing them would let a later call
    # with a different argument compute this entry's key and get this value back.
    args: tuple[Any, ...]
    kwargs: dict[str, Any]


def st_session_memo(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        cache_key = calc_cache_key(func, args, kwargs)

        if cache_key in st.session_state:
            entry: CacheEntry = st.session_state[cache_key]
            return entry.value

        value = func(*args, **kwargs)
        st.session_state[cache_key] = CacheEntry(value, args, kwargs)
        return value

    return inner

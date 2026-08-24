from __future__ import annotations

import functools
import uuid
from typing import TYPE_CHECKING, Any, Callable, ParamSpec, TypeVar, cast

import streamlit as st
from streamlit.runtime.caching.cache_type import CacheType
from streamlit.runtime.caching.cache_utils import _make_value_key

if TYPE_CHECKING:
    from types import FunctionType

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
    # `_make_value_key()` is the key builder behind `st.cache_data` and
    # `st.cache_resource`, so arguments are hashed here exactly as those decorators
    # hash theirs. It is a private API,
    # https://github.com/streamlit/streamlit/blob/1.44.0/lib/streamlit/runtime/caching/cache_utils.py,
    # whose signature took its current shape in Streamlit 1.25, the floor declared in
    # `pyproject.toml`. The cache type only selects which decorator name the
    # `UnhashableParamError` message suggests.
    value_key = _make_value_key(
        CacheType.RESOURCE,
        # Streamlit annotates this parameter as `FunctionType`, but only passes it to
        # `inspect.signature()` and reads `__name__` off it in the error path.
        cast("FunctionType", func),
        args,
        kwargs,
        None,
    )
    return f"{CACHE_KEY_PREFIX}-{get_fully_qualified_name(func)}-{value_key}"


def st_session_memo(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        cache_key = calc_cache_key(func, args, kwargs)

        if cache_key in st.session_state:
            cached: R = st.session_state[cache_key]
            return cached

        value = func(*args, **kwargs)
        st.session_state[cache_key] = value
        return value

    return inner

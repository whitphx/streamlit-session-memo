from __future__ import annotations

import functools
import sys
import uuid
from typing import TYPE_CHECKING, Any, Callable, TypeVar, cast

import streamlit as st
from streamlit.runtime.caching.cache_type import CacheType
from streamlit.runtime.caching.cache_utils import _make_value_key

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

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
    # The arguments are keyed by Streamlit's own key builder so that they are hashed
    # exactly like `st.cache_data` and `st.cache_resource` hash theirs: by content, so
    # that dicts and DataFrames key by value rather than by identity, skipping
    # parameters whose name starts with an underscore, and raising
    # `UnhashableParamError` for a type Streamlit cannot hash. It is a private API
    # (`streamlit/runtime/caching/cache_utils.py`) whose signature took its current
    # shape in Streamlit 1.25, the floor declared in `pyproject.toml`. The cache type
    # only selects which decorator name that error message suggests.
    # Streamlit annotates the parameter as `FunctionType`, but reads nothing off it
    # that any callable lacks.
    value_key = _make_value_key(
        CacheType.RESOURCE, cast("FunctionType", func), args, kwargs, None
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

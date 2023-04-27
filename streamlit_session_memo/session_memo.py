import uuid
from typing import Hashable

import streamlit as st


CACHE_KEY_PREFIX = uuid.uuid4().hex  # To make the key more unique even when args or kwargs are so simple


def get_fully_qualified_name(func):
    module_name = func.__module__
    qualname = func.__qualname__
    return f"{module_name}.{qualname}"


def calc_cache_key(func, args, kwargs) -> Hashable:
    hashable_args = [a if isinstance(a, Hashable) else id(a) for a in args]
    hashable_kwargs = {k: v if isinstance(v, Hashable) else id(v) for k, v in kwargs.items()}
    return CACHE_KEY_PREFIX, get_fully_qualified_name(func), tuple(hashable_args), tuple(sorted(hashable_kwargs.items()))


def st_session_memo(func):
    def inner(*args, **kwargs):
        cache_key = calc_cache_key(args, kwargs)

        if cache_key in st.session_state:
            return st.session_state[cache_key]

        value = func(*args, **kwargs)
        st.session_state[cache_key] = value
        return value

    return inner

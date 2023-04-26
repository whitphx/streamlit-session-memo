from typing import Hashable

import streamlit as st


def calc_cache_key(args, kwargs) -> Hashable:
    hashable_args = [a if isinstance(a, Hashable) else id(a) for a in args]
    hashable_kwargs = {k: v if isinstance(v, Hashable) else id(v) for k, v in kwargs.items()}
    return tuple(hashable_args), tuple(sorted(hashable_kwargs.items()))


def session_memo(func):
    def inner(*args, **kwargs):
        cache_key = calc_cache_key(args, kwargs)

        if cache_key in st.session_state:
            return st.session_state[cache_key]

        value = func(*args, **kwargs)
        st.session_state[cache_key] = value
        return value

    return inner

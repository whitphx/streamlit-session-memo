import typing

import pytest

from streamlit_session_memo.session_memo import calc_cache_key


class TestCalcCacheKey:
    @pytest.mark.parametrize("args, kwargs", [
        ((), {}),
        ((None,), {}),
        ((1,), {}),
        (("a",), {}),
        ((), {1: 1}),
        ((), {1: "a"}),
        ((), {1: None}),
        ((), {"a": 1}),
        ((), {"a": "b"}),
        ((), {"a": None}),
        ((1, 2, 3), {'a': 1, 'b': 2, 'c': 3})
    ])
    def test_hashable_arguments(self, args, kwargs):
        assert calc_cache_key(args, kwargs) == calc_cache_key(args, kwargs)
        assert isinstance(calc_cache_key(args, kwargs), typing.Hashable)

    def test_unhashable_arguments(self):
        assert calc_cache_key((object(),), {}) != calc_cache_key((object(),), {})
        assert isinstance(calc_cache_key((object(),), {}), typing.Hashable)

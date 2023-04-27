import typing

import pytest

from streamlit_session_memo.session_memo import calc_cache_key


TEST_ARGS_LIST = [
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
]


class TestCalcCacheKey:
    @pytest.mark.parametrize("args, kwargs", TEST_ARGS_LIST)
    def test_hashable_arguments(self, args, kwargs):
        def foo():
            pass

        assert calc_cache_key(foo, args, kwargs) == calc_cache_key(foo, args, kwargs)
        assert isinstance(calc_cache_key(foo, args, kwargs), typing.Hashable)

    @pytest.mark.parametrize("args, kwargs", TEST_ARGS_LIST)
    def test_with_different_functions(self, args, kwargs):
        def foo(a, b):
            pass

        def bar(a, b):
            pass

        assert calc_cache_key(foo, args, kwargs) != calc_cache_key(bar, args, kwargs)

    def test_unhashable_arguments(self):
        def foo():
            pass

        assert calc_cache_key(foo, (object(),), {}) != calc_cache_key(foo, (object(),), {})
        assert isinstance(calc_cache_key(foo, (object(),), {}), typing.Hashable)

import typing
from unittest.mock import Mock, patch

import pytest

from streamlit_session_memo.session_memo import calc_cache_key, st_session_memo

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
    ((1, 2, 3), {"a": 1, "b": 2, "c": 3}),
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

        assert calc_cache_key(foo, (object(),), {}) != calc_cache_key(
            foo, (object(),), {}
        )
        assert isinstance(calc_cache_key(foo, (object(),), {}), typing.Hashable)


@patch("streamlit_session_memo.session_memo.st")
def test_st_session_memo(st):
    st.session_state = {}

    spy = Mock()

    @st_session_memo
    def foo(a, b):
        spy()
        return a + b

    assert foo(1, 2) == 3
    spy.assert_called_once()

    spy.reset_mock()

    assert foo(1, 2) == 3
    spy.assert_not_called()

    spy.reset_mock()

    assert foo(1, 3) == 4
    spy.assert_called_once()

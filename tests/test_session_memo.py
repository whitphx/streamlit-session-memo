import typing
from unittest.mock import Mock, patch

import pytest
from streamlit.runtime.caching.cache_errors import UnhashableParamError

from streamlit_session_memo.session_memo import calc_cache_key, st_session_memo

TEST_ARGS_LIST = [
    ((), {}),
    ((None,), {}),
    ((1,), {}),
    (("a",), {}),
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

    def test_unhashable_arguments_are_keyed_by_content(self):
        def foo(config):
            pass

        assert calc_cache_key(foo, ({"a": 1},), {}) == calc_cache_key(
            foo, ({"a": 1},), {}
        )
        assert calc_cache_key(foo, ({"a": 1},), {}) != calc_cache_key(
            foo, ({"a": 2},), {}
        )

    def test_arguments_streamlit_cannot_hash(self):
        def foo(config):
            pass

        with pytest.raises(UnhashableParamError):
            calc_cache_key(foo, (object(),), {})

    def test_underscore_prefixed_parameters_are_skipped(self):
        def foo(_a, b):
            pass

        assert calc_cache_key(foo, (1, 2), {}) == calc_cache_key(foo, (9, 2), {})
        assert calc_cache_key(foo, (1, 2), {}) != calc_cache_key(foo, (1, 9), {})

    def test_positional_and_keyword_arguments_match(self):
        def foo(a, b):
            pass

        assert calc_cache_key(foo, (1, 2), {}) == calc_cache_key(
            foo, (), {"a": 1, "b": 2}
        )


@patch("streamlit_session_memo.session_memo.st")
def test_st_session_memo_with_unhashable_arguments(st):
    st.session_state = {}

    spy = Mock()

    @st_session_memo
    def foo(config):
        spy()
        return config["name"]

    # Each call builds an equal but distinct dict, as a rerun of a Streamlit script
    # would.
    assert [foo({"name": "a"}) for _ in range(3)] == ["a", "a", "a"]
    spy.assert_called_once()


def test_st_session_memo_preserves_function_metadata():
    @st_session_memo
    def foo(a, b):
        """Docstring of foo."""

    assert foo.__name__ == "foo"
    assert foo.__doc__ == "Docstring of foo."


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

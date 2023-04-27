# streamlit-session-memo

A decorator for session-specific caching on Streamlit.

```python
from streamlit_session_memo import st_session_memo


@st_session_memo
def load_big_model():
    ...
    return model


model = load_big_model()
```

This is a simple wrapper around `st.session_state` that caches the return value of the decorated function to the session state and returns the cached value if the function is called again with the same arguments.
We have been doing this manually with code like the following, but this decorator makes it simpler.
```python
# Boilerplate code for session-specific caching.
cache_key = f"{arg_1}_{arg_2}_{arg_3}"
if cache_key in st.session_state:
    model = st.session_state[cache_key]
else:
    result = load_expensive_model(arg_1, arg_2, arg_3)
    st.session_state[cache_key] = result
    model = result
```

Note that, this decorator is a lightweight wrapper around `st.session_state` that acts like the code snippet above, and does not provide any additional features such as mutation guards that `st.cache_data` provides.

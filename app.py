import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Tennis Club 6 Amici",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .block-container { padding: 0rem; max-width: 100%; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
""",
    unsafe_allow_html=True,
)

with open("index.html", "r", encoding="utf-8") as f:
  html_content = f.read()

components.html(html_content, height=850, scrolling=True)

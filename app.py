import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Tennis Club 6 Amici",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Rimuove i margini predefiniti di Streamlit
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

# Legge il file HTML esterno in modo sicuro al 100%
try:
  with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()
  components.html(html_content, height=850, scrolling=True)
except FileNotFoundError:
  st.error(
      "⚠️ Attenzione: il file 'index.html' non è stato trovato nel repository"
      " GitHub! Crealo o caricalo per visualizzare l'app."
  )

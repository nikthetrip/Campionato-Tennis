import base64
import json
import os
import requests
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

# Configurazione GitHub dalle Secrets di Streamlit
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
GITHUB_REPO = st.secrets.get("GITHUB_REPO", "")
GITHUB_FILE_PATH = st.secrets.get("GITHUB_FILE_PATH", "tennis_app_state.json")

API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def fetch_github_state():
  if not GITHUB_TOKEN or not GITHUB_REPO:
    return {}
  try:
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
      file_info = response.json()
      file_content = base64.b64decode(file_info["content"]).decode("utf-8")
      return json.loads(file_content)
  except Exception as e:
    print("Errore lettura:", e)
  return {}


# Leggi HTML base
with open("index.html", "r", encoding="utf-8") as f:
  html_content = f.read()

# Carica i dati attuali da GitHub e inietta i dati + configurazione GitHub nel browser
server_data = fetch_github_state()
json_str = json.dumps(server_data if server_data else {})

injection_script = f"""
<script>
    window.serverState = {json_str};
    window.githubConfig = {{
        token: "{GITHUB_TOKEN}",
        repo: "{GITHUB_REPO}",
        path: "{GITHUB_FILE_PATH}"
    }};
</script>
"""
html_content = html_content.replace("</head>", f"{injection_script}</head>")

components.html(html_content, height=850, scrolling=True)

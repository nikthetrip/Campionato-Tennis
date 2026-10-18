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

# Endpoint per le API di GitHub
API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}


# Gestione delle richieste POST inviate dall'interfaccia HTML (es. salvataggio partita)
query_params = st.query_params
if "action" in query_params and query_params["action"] == "save_state":
  try:
    # Legge il corpo della richiesta inviata dal browser
    body_bytes = st.context.headers.get("body", None)
    # In alternativa gestiamo i dati passati via session_state o query se necessario
    st.stop()
  except Exception as e:
    pass


# Funzione per leggere lo stato corrente da GitHub
def fetch_github_state():
  if not GITHUB_TOKEN or not GITHUB_REPO:
    return None
  try:
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
      file_info = response.json()
      file_content = base64.b64decode(file_info["content"]).decode("utf-8")
      return json.loads(file_content), file_info["sha"]
  except Exception as e:
    print("Errore lettura GitHub:", e)
  return None, None


# Legge l'HTML base
with open("index.html", "r", encoding="utf-8") as f:
  html_content = f.read()

# Carica i dati aggiornati da GitHub se disponibili
server_data, file_sha = fetch_github_state()
if server_data:
  json_str = json.dumps(server_data)
  injection_script = f"""
    <script>
        window.serverState = {json_str};
        window.githubMode = true;
    </script>
    """
  html_content = html_content.replace("</head>", f"{injection_script}</head>")

components.html(html_content, height=850, scrolling=True)

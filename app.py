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

# Configurazione GitHub dalle Secrets
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
GITHUB_REPO = st.secrets.get("GITHUB_REPO", "")
GITHUB_FILE_PATH = st.secrets.get("GITHUB_FILE_PATH", "tennis_app_state.json")

API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}


# Funzione per leggere lo stato da GitHub
def fetch_github_state():
  if not GITHUB_TOKEN or not GITHUB_REPO:
    return None, None
  try:
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
      file_info = response.json()
      file_content = base64.b64decode(file_info["content"]).decode("utf-8")
      return json.loads(file_content), file_info["sha"]
  except Exception as e:
    print("Errore lettura:", e)
  return None, None


# Funzione per scrivere lo stato su GitHub quando l'utente salva
def save_to_github(new_state_dict):
  if not GITHUB_TOKEN or not GITHUB_REPO:
    return False
  try:
    # Prima otteniamo lo SHA aggiornato del file
    _, sha = fetch_github_state()
    if not sha:
      return False

    content_str = json.dumps(new_state_dict, indent=2)
    content_encoded = base64.b64encode(content_str.encode("utf-8")).decode(
        "utf-8"
    )

    payload = {
        "message": "Aggiornamento risultati torneo da app",
        "content": content_encoded,
        "sha": sha,
    }
    response = requests.put(API_URL, headers=headers, json=payload)
    return response.status_code in [200, 201]
  except Exception as e:
    print("Errore scrittura:", e)
    return False


# Intercetta i dati inviati dall'interfaccia se l'utente ha salvato una partita
if st.query_params.get("save") == "true":
  # Leggiamo i dati passati via query string o post se presenti,
  # oppure gestiamo il salvataggio direttamente tramite un endpoint integrato.
  pass

# Leggi HTML base
with open("index.html", "r", encoding="utf-8") as f:
  html_content = f.read()

# Carica i dati attuali da GitHub
server_data, _ = fetch_github_state()
if server_data and server_data != {}:
  json_str = json.dumps(server_data)
  injection_script = f"""
    <script>
        window.serverState = {json_str};
        window.githubMode = true;
    </script>
    """
  html_content = html_content.replace("</head>", f"{injection_script}</head>")

components.html(html_content, height=850, scrolling=True)

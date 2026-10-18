import base64
import json
import urllib.request
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Tennis League 6 Amici", page_icon="🎾", layout="wide"
)

# Leggi le Secrets di Streamlit
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
GITHUB_REPO = st.secrets.get("GITHUB_REPO", "")
GITHUB_FILE_PATH = st.secrets.get("GITHUB_FILE_PATH", "tennis_app_state.json")

# Funzione per leggere l'ultimo stato direttamente da GitHub prima di caricare la pagina
latest_state = None
if GITHUB_TOKEN and GITHUB_REPO:
  url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"
  req = urllib.request.Request(
      url, headers={"Authorization": f"Bearer {GITHUB_TOKEN}"}
  )
  try:
    with urllib.request.urlopen(req) as response:
      if response.status == 200:
        data = json.loads(response.read().decode("utf-8"))
        content_str = base64.b64decode(data["content"]).decode("utf-8")
        latest_state = json.loads(content_str)
  except Exception as e:
    st.error(f"Errore lettura dati da GitHub: {e}")

# Inietta lo stato aggiornato e le credenziali nell'HTML
injection_script = f"""
<script>
    window.githubConfig = {{
        token: "{GITHUB_TOKEN}",
        repo: "{GITHUB_REPO}",
        path: "{GITHUB_FILE_PATH}"
    }};
    window.serverState = {json.dumps(latest_state) if latest_state else 'null'};
</script>
"""

# Leggi il file index.html
try:
  with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

  # Inserisci lo script di iniezione dentro l'head
  html_content = html_content.replace("</head>", f"{injection_script}</head>")

  # Renderizza il componente Streamlit
  components.html(html_content, height=1000, scrolling=True)

except FileNotFoundError:
  st.error("File index.html non trovato!")

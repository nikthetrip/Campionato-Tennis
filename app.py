import json
import os
import pandas as pd
import streamlit as st

DATA_FILE = "dati_torneo.json"

# Dati di default se il file non esiste
DEFAULT_DATA = {
    "giocatori": [
        "Amico 1",
        "Amico 2",
        "Amico 3",
        "Amico 4",
        "Amico 5",
        "Amico 6",
    ],
    "partite_campionato": [],
    "torneo_iniziato": False,
    "vincitore_torneo": "",
}


def carica_dati():
  if os.path.exists(DATA_FILE):
    try:
      with open(DATA_FILE, "r") as f:
        return json.load(f)
    except:
      return DEFAULT_DATA
  return DEFAULT_DATA


def salva_dati(data):
  with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=4)


# Inizializzazione stato
data = carica_dati()

st.set_page_config(
    page_title="Campionato & Torneo Tennis 6 Amici", page_icon="🎾", layout="wide"
)

st.title("🎾 Tennis Club: Campionato & Torneo Mensile")
st.markdown(
    "Gestione in tempo reale delle sfide a set unico tra 6 amici! Chiunque"
    " aggiorna il risultato, lo vede per primo."
)

# Sidebar per gestione giocatori
st.sidebar.header("👥 Gestione Giocatori")
nuovi_nomi = []
for i in range(6):
  nome = st.sidebar.text_input(
      f"Giocatore {i+1}", data["giocatori"][i], key=f"g_{i}"
  )
  nuovi_nomi.append(nome)

if st.sidebar.button("Aggiorna Nomi"):
  data["giocatori"] = nuovi_nomi
  salva_dati(data)
  st.sidebar.success("Nomi aggiornati!")
  st.rerun()

# Tab principali
tab1, tab2, tab3 = st.tabs(
    ["🏆 Campionato", "🎯 Torneo Mensile", "➕ Inserisci Risultato"]
)

# Calcolo Classifica Campionato
punti = {g: {"punti": 0, "vinte": 0, "perse": 0, "game_fatti": 0, "game_subiti": 0} for g in data["giocatori"]}

for p in data["partite_campionato"]:
  g1, g2, s1, s2 = p["g1"], p["g2"], p["g1_score"], p["g2_score"]
  if g1 in punti and g2 in punti:
    punti[g1]["game_fatti"] += s1
    punti[g1]["game_subiti"] += s2
    punti[g2]["game_fatti"] += s2
    punti[g2]["game_subiti"] += s1

    if s1 > s2:
      punti[g1]["vinte"] += 1
      punti[g2]["perse"] += 1
      if s2 == 5 or (s1 == 7 and s2 == 6):  # Tie break o vittoria tirata
        punti[g1]["punti"] += 2
        punti[g2]["punti"] += 1
      else:
        punti[g1]["punti"] += 3
    else:
      punti[g2]["vinte"] += 1
      punti[g1]["perse"] += 1
      if s1 == 5 or (s2 == 7 and s1 == 6):
        punti[g2]["punti"] += 2
        punti[g1]["punti"] += 1
      else:
        punti[g2]["punti"] += 3

df_classifica = pd.DataFrame.from_dict(punti, orient="index")
df_classifica["diff_game"] = (
    df_classifica["game_fatti"] - df_classifica["game_subiti"]
)
df_classifica = df_classifica.sort_values(
    by=["punti", "diff_game", "game_fatti"], ascending=False
).reset_index()
df_classifica.rename(columns={"index": "Giocatore"}, inplace=True)

with tab1:
  st.subheader("📊 Classifica Campionato (Set Unico)")
  if not data["partite_campionato"]:
    st.info("Nessuna partita giocata. Inserisci i risultati nella terza scheda!")
  
  # Mostra tabella formattata
  st.dataframe(
      df_classifica[[
          "Giocatore",
          "punti",
          "vinte",
          "perse",
          "game_fatti",
          "game_subiti",
          "diff_game",
      ]],
      use_container_width=True,
  )

  st.markdown("---")
  st.subheader("📜 Storico Partite Campionato")
  for idx, match in enumerate(data["partite_campionato"]):
    col1, col2 = st.columns([4, 1])
    with col1:
      st.write(
          f"🎾 **{match['g1']}** vs **{match['g2']}** ➔ Risultato: **{match['g1_score']} - {match['g2_score']}**"
      )
    with col2:
      if st.button("Elimina", key=f"del_c_{idx}"):
        data["partite_campionato"].pop(idx)
        salva_dati(data)
        st.rerun()

with tab3:
  st.subheader("➕ Registra Nuova Partita di Campionato")
  with st.form("form_partita"):
    col1, col2 = st.columns(2)
    with col1:
      giocatore1 = st.selectbox("Giocatore 1", data["giocatori"], index=0)
      score1 = st.number_input("Game vinti G1 (es. 6)", 0, 7, 6)
    with col2:
      # Filtra per evitare lo stesso giocatore
      altri = [g for g in data["giocatori"] if g != giocatore1]
      giocatore2 = st.selectbox("Giocatore 2", altri, index=0)
      score2 = st.number_input("Game vinti G2 (es. 4)", 0, 7, 4)

    submitted = st.form_submit_button("Registra Partita")
    if submitted:
      if giocatore1 == giocatore2:
        st.error("I due giocatori devono essere differenti!")
      elif score1 == score2:
        st.error("Il tennis non prevede pareggi a set singolo!")
      else:
        data["partite_campionato"].append({
            "g1": giocatore1,
            "g2": giocatore2,
            "g1_score": score1,
            "g2_score": score2,
        })
        salva_dati(data)
        st.success("Partita registrata con successo!")
        st.rerun()

with tab2:
  st.subheader("🎯 Tabellone Torneo Mensile")
  st.markdown(
      "Il tabellone si basa sulla classifica attuale del campionato (1° e 2°"
      " passano direttamente alle semifinali/BYE)."
  )

  giocatori_ordinati = df_classifica["Giocatore"].tolist()

  if len(giocatori_ordinati) == 6:
    st.markdown("### Quarti di Finale")
    col_q1, col_q2 = st.columns(2)
    with col_q1:
      st.info(
          f"**Match Q1:** 3° ({giocatori_ordinati[2]}) vs 6°"
          f" ({giocatori_ordinati[5]})"
      )
    with col_q2:
      st.info(
          f"**Match Q2:** 4° ({giocatori_ordinati[3]}) vs 5°"
          f" ({giocatori_ordinati[4]})"
      )

    st.markdown("### Semifinali")
    st.write(
        f"🔹 **Semifinale 1:** 1° ({giocatori_ordinati[0]}) vs Vincitore Match Q1"
    )
    st.write(
        f"🔹 **Semifinale 2:** 2° ({giocatori_ordinati[1]}) vs Vincitore Match Q2"
    )

    st.markdown("### Finale")
    st.write("🏆 Vincitore Semifinale 1 vs Vincitore Semifinale 2")
  else:
    st.warning("Assicurati di avere esattamente 6 giocatori attivi.")

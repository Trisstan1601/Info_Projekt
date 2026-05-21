import streamlit as st
import random

st.set_page_config(page_title="Schulprojekt: Ägypten Slot", page_icon="𓎡", layout="centered")
st.title("𓎡 Schulprojekt: 5-Walzen Ägypten-Slot")
st.write("Ein Prototyp zur Demonstration von 5-Walzen-Logik und Gewinnlinien.")

# --- INITIALISIERUNG ---
if "kontostand" not in st.session_state:
    st.session_state.kontostand = 500
if "linien" not in st.session_state:
    st.session_state.linien = 9
if "einsatz_pro_linie" not in st.session_state:
    st.session_state.einsatz_pro_linie = 2
if "freispiele" not in st.session_state:
    st.session_state.freispiele = 0

# Das 5x3 Raster mit Startsymbolen füllen
if "raster" not in st.session_state:
    st.session_state.raster = [
        ["❓", "❓", "❓", "❓", "❓"],
        ["❓", "❓", "❓", "❓", "❓"],
        ["❓", "❓", "❓", "❓", "❓"]
    ]

# Symbole mit unterschiedlichen Wertigkeiten (und das Buch)
SYMBOLE = {
    "🤠": "Forscher", 
    "👑": "Pharao", 
    "🦅": "Isis-Statue", 
    "𓄿": "Käfer", 
    "🅰️": "Ass", 
    "🦘": "König",
    "📖": "Buch (Scatter/Joker)"
}
Symbol_Liste = list(SYMBOLE.keys())

# --- EINSTELLUNGEN IN DER SEITENLEISTE ---
st.sidebar.header("Spieleinstellungen")
st.session_state.linien = st.sidebar.selectbox("Anzahl Gewinnlinien", [1, 3, 5, 9])
st.session_state.einsatz_pro_linie = st.sidebar.slider("Einsatz pro Linie", 1, 10, 2)

gesamteinsatz = st.session_state.linien * st.session_state.einsatz_pro_linie
st.sidebar.write(f"**Gesamteinsatz:** {gesamteinsatz} Punkte")

# --- SPIELLOGIK ---
def drehen():
    if st.session_state.kontostand < gesamteinsatz and st.session_state.freispiele == 0:
        st.error("Nicht genug Guthaben!")
        return

    if st.session_state.freispiele > 0:
        st.session_state.freispiele -= 1
    else:
        st.session_state.kontostand -= gesamteinsatz

    # Neues 5x3 Raster generieren
    neues_raster = []
    for reihe in range(3):
        neue_reihe = [random.choice(Symbol_Liste) for _ in range(5)]
        neues_raster.append(neue_reihe)
    
    st.session_state.raster = neues_raster

    # Zählen, wie viele Bücher (📖) auf dem Bildschirm sind
    anzahl_buecher = sum(reihe.count("📖") for reihe in neues_raster)
    
    if anzahl_buecher >= 3:
        st.session_state.freispiele += 10
        st.balloons()
        st.success(f"𓋹 {anzahl_buecher} BÜCHER! Du hast 10 FREISPIELE gewonnen! 𓋹")

# --- UI ANZEIGE ---
st.metric(label="Kontostand", value=f"{st.session_state.kontostand} Punkte")
if st.session_state.freispiele > 0:
    st.info(f"✨ Verbleibende Freispiele: {st.session_state.freispiele} ✨")

st.markdown("---")

# Das 5x3 Raster anzeigen
for r in range(3):
    cols = st.columns(5)
    for c in range(5):
        with cols[c]:
            st.markdown(f"<h2 style='text-align: center; background-color: #1e1e1e; padding: 10px; border-radius: 5px;'>{st.session_state.raster[r][c]}</h2>", unsafe_allow_html=True)

st.markdown("---")

if st.button("𓀚 Start (Drehen)", use_container_width=True):
    drehen()

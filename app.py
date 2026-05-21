import streamlit as st
import random
import time

# --- SEITENKONFIGURATION ---
st.set_page_config(page_title="Schulprojekt: Slot Machine", page_icon="🎰", layout="centered")

st.title("🎰 Schulprojekt: Mini Slot Machine")
st.write("Willkommen beim Prototypen! Drücke auf 'Drehen', um dein Glück zu versuchen.")

# --- INITIALISIERUNG DES ZUSTANDS (Session State) ---
# Hier speichern wir Daten, die zwischen den Klicks erhalten bleiben müssen.
if "geld" not in st.session_state:
    st.session_state.geld = 100

if "kontostand" not in st.session_state:
    st.session_state.kontostand = 100  # Startguthaben

if "walzen" not in st.session_state:
    st.session_state.walzen = ["🍒", "🍋", "🍇"]  # Start-Symbole auf dem Bildschirm

# Mögliche Symbole auf den Walzen
SYMBOLE = ["🍒", "🍋", "🍇", "🔔", "💎", "7️⃣"]

# --- SPIELLOGIK ---
def drehen():
    # Prüfen, ob noch Guthaben da ist
    if st.session_state.kontostand <= 0:
        st.error("Du hast kein Guthaben mehr! Setze das Spiel zurück.")
        return

    # Einsatz abziehen
    st.session_state.kontostand -= 10

    # Zufällige Auswahl für die drei Walzen
    w1 = random.choice(SYMBOLE)
    w2 = random.choice(SYMBOLE)
    w3 = random.choice(SYMBOLE)
    
    st.session_state.walzen = [w1, w2, w3]

    # Gewinnberechnung
    if w1 == w2 == w3:
        # Hauptgewinn bei 3 gleichen Symbolen
        if w1 == "7️⃣":
            gewinn = 100
        elif w1 == "💎":
            gewinn = 70
        else:
            gewinn = 40
        st.session_state.kontostand += gewinn
        st.success(f"🎉 JACKPOT! 3x {w1}! Du gewinnst {gewinn} Punkte!")
    elif w1 == w2 or w2 == w3 or w1 == w3:
        # Kleiner Gewinn bei 2 gleichen Symbolen
        st.session_state.kontostand += 15
        st.info("✨ Gut gemacht! 2 gleiche Symbole! Du gewinnst 15 Punkte!")
    else:
        st.warning("Leider kein Gewinn. Versuch es noch einmal!")

# --- BENUTZEROBERFLÄCHE (UI) ---

# Anzeige des aktuellen Kontostands
st.metric(label="Dein Guthaben", value=f"{st.session_state.kontostand} Punkte")
st.metric(label="Dein Geld", value=f"{st.session_state.geld} ID")

st.markdown("---")

# Schöne Darstellung der Walzen in Spalten (Columns)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.walzen[0]}</h1>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.walzen[1]}</h1>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.walzen[2]}</h1>", unsafe_allow_html=True)

st.markdown("---")

# Buttons für die Steuerung
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    # Der Dreh-Button (kostet 10 Punkte)
    if st.button("🎰 Jetzt Drehen! (Kosten: 10 Punkte)", use_container_width=True):
        drehen()

with col_btn2:
    # Reset-Button, um das Spiel neu zu starten
    if st.button("🔄 Spiel zurücksetzen", use_container_width=True):
        st.session_state.geld = 100
        st.session_state.kontostand = 100
        st.session_state.walzen = ["🍒", "🍋", "🍇"]
        st.rerun()

st.markdown("---")

col_btn1 = st.columns(1)

with col_btn1:
    if st.button("Jetzt neues Guthaben kaufen! (5ID = 100 Punkte)", use_container_width=True):
        st.session_state.kontostand + 100
        st.session_state.geld - 5

# --- ANLEITUNG / ERKLÄRUNG FÜR DIE SCHULE ---
st.markdown("### ℹ️ Spielregeln & Infos")
st.write("""
- **Einsatz:** Jeder Dreh kostet dich 10 Punkte.
- **2 gleiche Symbole:** Du erhältst 15 Punkte zurück.
- **3 gleiche Symbole:** Großer Gewinn! (Je nach Symbol zwischen 40 und 100 Punkten).
- Dieses Projekt wurde zu Bildungszwecken mit Python und Streamlit erstellt.
""")

import streamlit as st
import random
import time

st.set_page_config(page_title="Schulprojekt: Slot Machine", page_icon="🎰", layout="centered")

st.title("🎰 GIG: Glücksspiel ist Geil")
st.write("Willkommen beim Schul-Casino! Drücke auf 'Drehen', um dein Glück zu versuchen.")

if "geld" not in st.session_state:
    st.session_state.geld = 100

if "kontostand" not in st.session_state:
    st.session_state.kontostand = 100  # Startguthaben

if "walzen" not in st.session_state:
    st.session_state.walzen = ["🍒", "🍋", "🍇"]  

SYMBOLE = ["🍒", "🍋", "🍇", "🔔", "💎", "7️⃣"]

def drehen(aktueller_einsatz):
    if st.session_state.kontostand <= 0:
        st.error("Du hast kein Guthaben mehr! Setze das Spiel zurück.")
        return

    st.session_state.kontostand -= aktueller_einsatz

    w1 = random.choice(SYMBOLE)
    w2 = random.choice(SYMBOLE)
    w3 = random.choice(SYMBOLE)
    
    st.session_state.walzen = [w1, w2, w3]

    w1, w2, w3 = st.session_state.walzen

    if w1 == w2 == w3:
        if w1 == "7️⃣":
            gewinn = aktueller_einsatz*10
        elif w1 == "💎":
            gewinn = aktueller_einsatz*7
        else:
            gewinn = aktueller_einsatz*4
        st.session_state.kontostand += gewinn
        st.success(f"🎉 JACKPOT! 3x {w1}! Du gewinnst {gewinn} Punkte!")
        st.rerun()
        
    elif w1 == w2 or w2 == w3 or w1 == w3:
        st.session_state.kontostand += 15
        st.info("✨ Gut gemacht! 2 gleiche Symbole! Du gewinnst 15 Punkte!")
        st.rerun() 
    else:
        st.warning("Leider kein Gewinn. Versuch es noch einmal!")
        st.rerun()


st.metric(label="Dein Guthaben", value=f"{st.session_state.kontostand} Punkte")
st.metric(label="Dein Geld", value=f"{st.session_state.geld} ID")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.walzen[0]}</h1>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.walzen[1]}</h1>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.walzen[2]}</h1>", unsafe_allow_html=True)


einsatz = st.selectbox("Wähle deinen Einsatz:", [5, 10, 20, 50])


st.markdown("---")

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("🎰 Jetzt Drehen!", use_container_width=True):
        drehen(einsatz)

with col_btn2:
    if st.button("🔄 Spiel zurücksetzen", use_container_width=True):
        st.session_state.geld = 100
        st.session_state.kontostand = 100
        st.session_state.walzen = ["🍒", "🍋", "🍇"]
        st.rerun()

st.markdown("---")

col_shop = st.columns(1)

with col_shop[0]:
    if st.button("Jetzt neues Guthaben kaufen! (5ID = 100 Punkte)", use_container_width=True):
        if st.session_state.geld >= 5:
            st.session_state.kontostand += 100  
            st.session_state.geld -= 5          
            st.rerun()                         
        else:
            st.error("Du hast nicht genug ID, um Guthaben zu kaufen!")

st.markdown("### ℹ️ Spielregeln & Infos")
st.write("""
- **Einsatz:** Jeder Dreh kostet dich 10 Punkte.
- **2 gleiche Symbole:** Du erhältst 15 Punkte zurück.
- **3 gleiche Symbole:** Großer Gewinn! (Je nach Symbol zwischen 40 und 100 Punkten).
- Dieses Projekt wurde zu Bildungszwecken mit Python und Streamlit erstellt.
""")



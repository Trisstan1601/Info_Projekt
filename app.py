import streamlit as st
import random

st.set_page_config(
    page_title="Schulprojekt: Casino",
    page_icon="🎰",
    layout="centered"
)

# =====================================================
# Session State Initialisierung
# =====================================================

if "geld" not in st.session_state:
    st.session_state.geld = 100

if "kontostand" not in st.session_state:
    st.session_state.kontostand = 100

if "walzen" not in st.session_state:
    st.session_state.walzen = ["🍒", "🍋", "🍇"]

if "bj_spiel_laeuft" not in st.session_state:
    st.session_state.bj_spiel_laeuft = False

if "bj_eigene_karten" not in st.session_state:
    st.session_state.bj_eigene_karten = []

if "bj_dealer_karten" not in st.session_state:
    st.session_state.bj_dealer_karten = []

if "bj_status_text" not in st.session_state:
    st.session_state.bj_status_text = ""

if "bj_spiel_einsatz" not in st.session_state:
    st.session_state.bj_spiel_einsatz = 0


# =====================================================
# SLOT MACHINE
# =====================================================

SYMBOLE = ["🍒", "🍋", "🍇", "🔔", "💎", "7️⃣"]

def drehen(einsatz):

    if st.session_state.kontostand <= 0:
        st.error("Du hast kein Guthaben mehr!")
        return

    if st.session_state.kontostand < einsatz:
        st.error("Nicht genügend Guthaben!")
        return

    st.session_state.kontostand -= einsatz

    w1 = random.choice(SYMBOLE)
    w2 = random.choice(SYMBOLE)
    w3 = random.choice(SYMBOLE)

    st.session_state.walzen = [w1, w2, w3]

    if w1 == w2 == w3:

        if w1 == "7️⃣":
            gewinn = einsatz * 10
        elif w1 == "💎":
            gewinn = einsatz * 7
        else:
            gewinn = einsatz * 4

        st.session_state.kontostand += gewinn
        st.success(f"🎉 JACKPOT! Du gewinnst {gewinn} Punkte!")

    elif w1 == w2 or w2 == w3 or w1 == w3:

        gewinn = int(einsatz * 1.5)
        st.session_state.kontostand += gewinn

        st.info(f"✨ Zwei gleiche Symbole! Gewinn: {gewinn} Punkte")

    else:
        st.warning("Leider kein Gewinn.")


def slot_machine():

    st.title("🎰 Slot Machine")

    st.metric(
        "Dein Guthaben",
        f"{st.session_state.kontostand} Punkte"
    )

    st.metric(
        "Dein Geld",
        f"{st.session_state.geld} ID"
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"<h1 style='text-align:center'>{st.session_state.walzen[0]}</h1>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"<h1 style='text-align:center'>{st.session_state.walzen[1]}</h1>",
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"<h1 style='text-align:center'>{st.session_state.walzen[2]}</h1>",
            unsafe_allow_html=True
        )

    einsatz = st.selectbox(
        "Wähle deinen Einsatz:",
        [5, 10, 20, 50]
    )

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("🎰 Jetzt drehen"):
            drehen(einsatz)

    with col_b:
        if st.button("🔄 Zurücksetzen"):

            st.session_state.kontostand = 100
            st.session_state.geld = 100
            st.session_state.walzen = ["🍒", "🍋", "🍇"]

            st.rerun()

    st.markdown("---")

    if st.button("💰 100 Punkte für 5 ID kaufen"):

        if st.session_state.geld >= 5:

            st.session_state.geld -= 5
            st.session_state.kontostand += 100

            st.success("100 Punkte gekauft!")

        else:
            st.error("Nicht genügend ID!")

    st.markdown("---")

    st.subheader("ℹ️ Spielregeln")

    st.write("""
    - 2 gleiche Symbole → 1.5x Einsatz
    - 3 gleiche Symbole → 4x bis 10x Einsatz
    - 5 ID = 100 Punkte
    """)


# =====================================================
# BLACKJACK
# =====================================================

ZAHLEN = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]


def blackjack_starten(einsatz):

    if st.session_state.kontostand < einsatz:
        st.error("Nicht genügend Guthaben!")
        return

    st.session_state.kontostand -= einsatz

    st.session_state.bj_spiel_einsatz = einsatz

    st.session_state.bj_eigene_karten = [
        random.choice(ZAHLEN),
        random.choice(ZAHLEN)
    ]

    st.session_state.bj_dealer_karten = [
        random.choice(ZAHLEN),
        random.choice(ZAHLEN)
    ]

    st.session_state.bj_spiel_laeuft = True
    st.session_state.bj_status_text = "Spiel läuft."


def dealer_spielt():

    spieler = sum(st.session_state.bj_eigene_karten)
    dealer = sum(st.session_state.bj_dealer_karten)

    while dealer < 17:
        st.session_state.bj_dealer_karten.append(
            random.choice(ZAHLEN)
        )
        dealer = sum(st.session_state.bj_dealer_karten)

    if dealer > 21:

        st.session_state.bj_status_text = (
            f"🎉 Dealer überkauft ({dealer})"
        )

        st.session_state.kontostand += (
            st.session_state.bj_spiel_einsatz * 2
        )

    elif spieler > dealer:

        st.session_state.bj_status_text = (
            f"🎉 Du gewinnst ({spieler} : {dealer})"
        )

        st.session_state.kontostand += (
            st.session_state.bj_spiel_einsatz * 2
        )

    elif dealer > spieler:

        st.session_state.bj_status_text = (
            f"😞 Dealer gewinnt ({dealer} : {spieler})"
        )

    else:

        st.session_state.bj_status_text = (
            f"🤝 Unentschieden ({spieler} : {dealer})"
        )

        st.session_state.kontostand += (
            st.session_state.bj_spiel_einsatz
        )

    st.session_state.bj_spiel_laeuft = False


def blackjack():

    st.title("🃏 Blackjack")

    st.metric(
        "Dein Guthaben",
        f"{st.session_state.kontostand} Punkte"
    )

    einsatz = st.selectbox(
        "Wähle deinen Einsatz:",
        [5, 10, 20, 50],
        key="bj_einsatz"
    )

    if not st.session_state.bj_spiel_laeuft:

        if st.button("🃏 Neues Spiel starten"):
            blackjack_starten(einsatz)
            st.rerun()

    if st.session_state.bj_eigene_karten:

        spieler = sum(st.session_state.bj_eigene_karten)

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("🤵 Dealer")

            if st.session_state.bj_spiel_laeuft:

                st.write(
                    f"Karten: [{st.session_state.bj_dealer_karten[0]}, ?]"
                )

            else:

                st.write(
                    st.session_state.bj_dealer_karten
                )

        with col2:

            st.subheader("👤 Spieler")

            st.write(
                st.session_state.bj_eigene_karten
            )

            st.write(
                f"Summe: {spieler}"
            )

        st.markdown("---")

        if st.session_state.bj_status_text:
            st.info(st.session_state.bj_status_text)

        if st.session_state.bj_spiel_laeuft:

            col_a, col_b = st.columns(2)

            with col_a:

                if st.button("➕ Hit"):

                    st.session_state.bj_eigene_karten.append(
                        random.choice(ZAHLEN)
                    )

                    if sum(st.session_state.bj_eigene_karten) > 21:

                        st.session_state.bj_status_text = (
                            "💥 Überkauft! Dealer gewinnt."
                        )

                        st.session_state.bj_spiel_laeuft = False

                    st.rerun()

            with col_b:

                if st.button("🛑 Stand"):
                    dealer_spielt()
                    st.rerun()


# =====================================================
# HAUPTMENÜ
# =====================================================

st.sidebar.title("🎮 Spielauswahl")

spiel_auswahl = st.sidebar.selectbox(
    "Wähle ein Spiel:",
    [
        "🎰 Slot Machine",
        "🃏 Blackjack"
    ]
)

if spiel_auswahl == "🎰 Slot Machine":
    slot_machine()

elif spiel_auswahl == "🃏 Blackjack":
    blackjack()

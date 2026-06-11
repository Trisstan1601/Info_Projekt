import streamlit as st
import random
import time

st.set_page_config(page_title="Schulprojekt: Slot Machine", page_icon="🎰", layout="centered")

spiel_auswahl = st.sidebar.selectbox(
    "Wähle ein Spiel:",
    ["🎰 Slot Machine", "🃏 Schwarzer Joachim", "🪙 Coin Flip"]
)

if spiel_auswahl == "🎰 Slot Machine":
    def slot_machine():
        if "geld" not in st.session_state:
            st.session_state.geld = 100
        
        if "kontostand" not in st.session_state:
            st.session_state.kontostand = 100  # Startguthaben
        
        if "walzen" not in st.session_state:
            st.session_state.walzen = ["🍒", "🍋", "🍇"]  
        
        SYMBOLE = ["🍒", "🍋", "🍇", "🔔", "💎", "7️⃣"]
        
        def drehen(aktueller_einsatz):
            if st.session_state.kontostand <= 0:
                st.error("Du hast kein Guthaben mehr! Kaufe dir weiteres Guthaben.")
                return
            elif st.session_state.kontostand < aktueller_einsatz:
                st.error("Wähle einen anderen Einsatz.")
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
                st.session_state.kontostand += aktueller_einsatz*1.5
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
            if st.button("🔄 Spiel zurücksetzen", use_container_width=True, type="primary"):
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
    slot_machine()
    pass
elif spiel_auswahl == "🃏 Schwarzer Joachim":
    def blackjack():
        if "kontostand" not in st.session_state:
            st.session_state.kontostand = 100
        
        if "bj_spiel_laeuft" not in st.session_state:
            st.session_state.bj_spiel_laeuft = False
        
        if "bj_eigene_karten" not in st.session_state:
            st.session_state.bj_eigene_karten = []
        
        if "bj_dealer_karten" not in st.session_state:
            st.session_state.bj_dealer_karten = []
        
        if "bj_status_text" not in st.session_state:
            st.session_state.bj_status_text = ""
        
        # Kartendeck (Zahlenwerte)
        ZAHLEN = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] # Optional die 11 für das Ass hinzugefügt
        
        def blackjack_starten(einsatz_bj):
            """Startet eine neue Runde Blackjack und zieht den Einsatz ab."""
            if st.session_state.kontostand < einsatz_bj:
                st.error("Nicht genug Guthaben für diesen Einsatz!")
                return
            
            st.session_state.kontostand -= einsatz_bj
            st.session_state.bj_spiel_einsatz = einsatz_bj
            
            # Karten für Spieler und Dealer neu austeilen
            st.session_state.bj_eigene_karten = [random.choice(ZAHLEN), random.choice(ZAHLEN)]
            st.session_state.bj_dealer_karten = [random.choice(ZAHLEN), random.choice(ZAHLEN)]
            
            st.session_state.bj_spiel_laeuft = True
            st.session_state.bj_status_text = "Spiel läuft. Möchtest du noch eine Karte?"
            st.rerun()
        
        def dealer_spielt():
            """Die Logik für den Dealer, wenn der Spieler 'Halten' drückt."""
            eigene_summe = sum(st.session_state.bj_eigene_karten)
            dealer_summe = sum(st.session_state.bj_dealer_karten)
            
            # Dealer zieht bis mindestens 17
            while dealer_summe < 17:
                st.session_state.bj_dealer_karten.append(random.choice(ZAHLEN))
                dealer_summe = sum(st.session_state.bj_dealer_karten)
                
            # Gewinnprüfung
            if dealer_summe > 21:
                st.session_state.bj_status_text = f"🎉 Dealer hat sich überkauft ({dealer_summe})! Du gewinnst!"
                st.session_state.kontostand += st.session_state.bj_spiel_einsatz * 2
            elif dealer_summe > eigene_summe:
                st.session_state.bj_status_text = f"😞 Dealer gewinnt mit {dealer_summe} gegen {eigene_summe}."
            elif eigene_summe > dealer_summe:
                st.session_state.bj_status_text = f"🎉 Du gewinnst mit {eigene_summe} gegen {dealer_summe}!"
                st.session_state.kontostand += st.session_state.bj_spiel_einsatz * 2
            else:
                st.session_state.bj_status_text = f"🤝 Unentschieden ({eigene_summe} : {dealer_summe}). Einsatz zurück!"
                st.session_state.kontostand += st.session_state.bj_spiel_einsatz
                
            st.session_state.bj_spiel_laeuft = False
            st.rerun()
        
        
        st.title("🃏 Schul-Casino: Black Jack")
        st.metric(label="Dein Guthaben", value=f"{st.session_state.kontostand} Punkte")
        
        einsatz_bj = st.selectbox("Wähle deinen Blackjack-Einsatz:", [5, 10, 20, 50], key="bj_einsatz_select")
        
        if not st.session_state.bj_spiel_laeuft:
            if st.button("🃏 Neues Spiel starten", use_container_width=True):
                blackjack_starten(einsatz_bj)
        
        if st.session_state.bj_eigene_karten:
            st.markdown("---")
            
            eigene_summe = sum(st.session_state.bj_eigene_karten)
            dealer_summe = sum(st.session_state.bj_dealer_karten)
            
            col_dealer, col_spieler = st.columns(2)
            
            with col_dealer:
                st.markdown("### 🤵 Dealer Karten")
                if st.session_state.bj_spiel_laeuft:
                    st.write(f"Karten: [{st.session_state.bj_dealer_karten[0]}, ?]")
                    st.write(f"Sichtbare Summe: {st.session_state.bj_dealer_karten[0]}")
                else:
                    st.write(f"Karten: {st.session_state.bj_dealer_karten}")
                    st.write(f"Gesamtsumme: {dealer_summe}")
                    
            with col_spieler:
                st.markdown("### 👤 Deine Karten")
                st.write(f"Karten: {st.session_state.bj_eigene_karten}")
                st.write(f"Deine Summe: {eigene_summe}")
        
            st.markdown("---")
            
            if not st.session_state.bj_spiel_laeuft:
                if "🎉" in st.session_state.bj_status_text:
                    st.success(st.session_state.bj_status_text)
                elif "🤝" in st.session_state.bj_status_text:
                    st.info(st.session_state.bj_status_text)
                else:
                    st.warning(st.session_state.bj_status_text)
            else:
                st.info(st.session_state.bj_status_text)
        
            if st.session_state.bj_spiel_laeuft:
                col_hit, col_stand = st.columns(2)
                
                with col_hit:
                    if st.button("➕ Karte ziehen (Hit)", use_container_width=True):
                        st.session_state.bj_eigene_karten.append(random.choice(ZAHLEN))
                        if sum(st.session_state.bj_eigene_karten) > 21:
                            st.session_state.bj_status_text = f"💥 Überkauft ({sum(st.session_state.bj_eigene_karten)})! Der Dealer gewinnt."
                            st.session_state.bj_spiel_laeuft = False
                        st.rerun()
                        
                with col_stand:
                    if st.button("🛑 Keine Karte mehr (Stand)", use_container_width=True):
                        dealer_spielt()
    blackjack()
    pass
/*elif spiel_auswahl == "🪙 Coin Flip":
# Spielzustand initialisieren (damit die Computerwahl stabil bleibt)
if "computer_wahl" not in st.session_state:
    st.session_state.computer_wahl = random.choice([1, 2])

# Benutzereingabe über ein Radio-Button-Auswahlfeld
antwort = st.radio("Bitte wähle Kopf oder Zahl:", ("Kopf", "Zahl"))

# Spieler-Wahl zuweisen
if antwort == "Kopf":
    spieler_wahl = 1
else:
    spieler_wahl = 2

# Button zum Spielen
if st.button("Münze werfen!"):
    # Ergebnis prüfen
    if st.session_state.computer_wahl == spieler_wahl:
        st.success(f"🎉 {antwort}! Du hast gewonnen. Einsatz verdoppelt!")
    else:
        st.error(f"😢 Leider nicht {antwort}! Du hast verloren.") */

    # Nach dem Spiel die Computerwahl für die nächste Runde neu auslosen
    st.session_state.computer_wahl = random.choice([1, 2])
    st.markdown("### ℹ️ Spielregeln & Infos")
    st.write("""
    - **Einsatz:** Jeder Dreh kostet dich deinen ausgewählten Einsatz.
    - **2 gleiche Symbole:** Du erhältst 1.5x deinen Einsatz zurück.
    - **3 gleiche Symbole:** Großer Gewinn! (Je nach Symbol zwischen 4x und 10x deinen Einsatz).
    - **5 Informatik Dollar (ID)** können **100 Punkte** kaufen.
    - Dieses Projekt wurde ausschließlich zu Bildungszwecken mit Python und Streamlit erstellt.
    """)



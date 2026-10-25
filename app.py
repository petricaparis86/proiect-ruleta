import random
import time
import streamlit as st

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(page_title="Roulette Auto Pândă Dynamic", page_icon="🎰", layout="centered")

# --- CONFIGURARE PAROLĂ ---
PAROLA_CORECTA = "Ruleta2026"

if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False

if not st.session_state["autentificat"]:
    st.title("🔒 Acces Restricționat")
    parola_introdusa = st.text_input("Introdu parola pentru a accesa softul:", type="password")
    if st.button("Conectare", use_container_width=True):
        if parola_introdusa == PAROLA_CORECTA:
            st.session_state["autentificat"] = True
            st.rerun()
        else:
            st.error("Parolă incorectă!")
    st.stop()

# --- GENERARE DINAMICĂ LA FIECARE SESIUNE NOUĂ ---
if "baza_date_grupuri" not in st.session_state:
    toate_numerele_ruleta = list(range(0, 37))

    # !!! ELEMENTUL CHEIE: Folosește timpul curent ca seed pentru a genera grupuri NOI de fiecare dată
    random.seed(time.time())

    st.session_state["baza_date_grupuri"] = [
        set(random.sample(toate_numerele_ruleta, 18)) for _ in range(1_000_000)
    ]

# --- CODUL APLICAȚIEI AUTOMATE ---
st.title("⚡ Scanner Auto-Dynamic 1M")
st.write("Generare unică la pornire. Softul scanează **1.000.000 de grupuri complet NOI în această sesiune**. Pândă la **22 de tururi**.")

if st.button("🔓 Deconectare / Schimbă Grupurile", type="secondary"):
    # Ștergem stările salvate pentru a forța generarea de grupuri noi la următoarea logare
    st.session_state["autentificat"] = False
    if "baza_date_grupuri" in st.session_state:
        del st.session_state["baza_date_grupuri"]
    if "istoric_live" in st.session_state:
        del st.session_state["istoric_live"]
    st.rerun()

st.divider()

# --- MEMORIE PENTRU ISTORICUL LIVE ---
if "istoric_live" not in st.session_state:
    st.session_state["istoric_live"] = []

# --- ZONA DE INTRODUCERE NUMERE ---
st.write("### ➕ Adaugă numărul extras:")
col_input, col_btn = st.columns()

with col_input:
    numar_nou = st.number_input("Număr (0-36):", min_value=0, max_value=36, step=1, value=0, key="numar_input")

declanseaza_scanare = False

with col_btn:
    st.write("##")
    if st.button("Adaugă Număr", use_container_width=True):
        st.session_state["istoric_live"].append(numar_nou)
        declanseaza_scanare = True

# --- AFIȘARE ISTORIC ACTUAL ---
if st.session_state["istoric_live"]:
    st.write("**Istoricul tău actual (de la cel mai vechi la cel mai recent):**")
    st.info(" ➡️ ".join(map(str, st.session_state["istoric_live"])))

    if st.button("🗑️ Șterge tot istoricul (Reset)", type="primary"):
        st.session_state["istoric_live"] = []
        st.rerun()
else:
    st.warning("⚠️ Istoricul este gol. Introdu numerele extrase pentru a porni scanarea.")

st.divider()

# --- PROCESARE AUTOMATĂ INSTANTANEE ---
if st.session_state["istoric_live"]:
    st.write("### 🔍 Stare Alerte Pândă (Scanat în 1.000.000 de grupuri noi):")

    timp_start = time.time()
    istoric = st.session_state["istoric_live"]
    grupuri_baza = st.session_state["baza_date_grupuri"]

    grupuri_in_pinda_gasite = []
    cea_mai_mare_intarziere = 0

    for grup_curent in grupuri_baza:
        intarziere_curenta = 0
        for numar in reversed(istoric):
            if numar in grup_curent:
                break
            else:
                intarziere_curenta += 1

        if intarziere_curenta > cea_mai_mare_intarziere:
            cea_mai_mare_intarziere = intarziere_curenta

        if intarziere_curenta >= 22:
            if len(grupuri_in_pinda_gasite) < 3 and grup_curent not in [g for g in grupuri_in_pinda_gasite]:
                grupuri_in_pinda_gasite.append((grup_curent, intarziere_curenta))

    durata_totala = time.time() - timp_start

    st.metric("Cea mai mare întârziere activă înregistrată acum", f"{cea_mai_mare_intarziere} tururi")

    if grupuri_in_pinda_gasite:
        st.error("🚨 ALERTĂ: AU FOST DETECTATE GRUPURI ÎN PÂNDĂ CRITICĂ!")
        for idx, (grup, intarziere) in enumerate(grupuri_in_pinda_gasite, 1):
            st.write(f"🎯 **Grupul Sugerat #{idx} (Lipsește de {intarziere} tururi):**")
            st.code(str(sorted(list(grup))))
            st.write("---")
    else:
        st.info("ℹ️ Niciun grup din acest milion curent nu a atins pragul de 22 de tururi. Adaugă următorul număr.")

    if declanseaza_scanare:
        st.toast(f"Număr înregistrat! Scanare completă în {durata_totala:.4f}s", icon="⚡")

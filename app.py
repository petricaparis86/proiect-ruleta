import random
import time
import streamlit as st

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(page_title="Roulette Live Pândă", page_icon="🎰", layout="centered")

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

# --- CODUL APLICAȚIEI ---
st.title("🎰 Scanner Live - 20 Milioane Grupuri")
st.write("Introdu numerele extrase live la masă. Softul scanează instant cele 20M de grupuri pentru întârzieri de **22 de tururi**.")

if st.button("🔓 Deconectare", type="secondary"):
    st.session_state["autentificat"] = False
    st.rerun()

st.divider()

# --- MEMORIE PENTRU ISTORICUL LIVE ---
if "istoric_live" not in st.session_state:
    st.session_state["istoric_live"] = []

# --- ZONA DE INTRODUCERE NUMERE (OPTIMIZATĂ PENTRU TELEFON) ---
st.write("### ➕ Adaugă numărul extras la masă:")
col_input, col_btn = st.columns([2, 1])

with col_input:
    numar_nou = st.number_input("Număr (0-36):", min_value=0, max_value=36, step=1, value=0, key="numar_input")

with col_btn:
    st.write("##") # Spațiere pentru aliniere buton
    if st.button("Adaugă Număr", use_container_width=True):
        st.session_state["istoric_live"].append(numar_nou)
        st.success(f"Adăugat: {numar_nou}")
        st.rerun()

# --- AFIȘARE ISTORIC ACTUAL ---
if st.session_state["istoric_live"]:
    st.write("**Istoricul tău actual (de la cel mai vechi la cel mai recent):**")
    st.info(" ➡️ ".join(map(str, st.session_state["istoric_live"])))

    if st.button("🗑️ Șterge tot istoricul (Reset)", type="primary"):
        st.session_state["istoric_live"] = []
        st.rerun()
else:
    st.warning("⚠️ Istoricul este gol. Introdu primele numere extrase pentru a porni scanarea.")

st.divider()

# --- BUTON SCANARE PROPRIU-ZISĂ ---
if st.session_state["istoric_live"]:
    st.write("### 🔍 Scanare baze de date grupuri")

    if st.button("⚡ SCANEAZĂ CELE 20M DE GRUPURI", use_container_width=True):
        status_text = st.empty()
        progress_bar = st.progress(0)

        timp_start = time.time()
        istoric = st.session_state["istoric_live"]

        total_grupuri_tinta = 20_000_000
        BATCH_SIZE = 250_000
        toate_numerele_ruleta = list(range(0, 37))

        grupuri_in_pinda_gasite = []
        cea_mai_mare_intarziere = 0

        # Generăm grupuri cu un seed fix bazat pe numărul de grupuri, pentru a păstra constanța bazei de date virtuale
        random.seed(42)

        for batch in range(total_grupuri_tinta // BATCH_SIZE):
            for _ in range(BATCH_SIZE):
                # Generăm grupul unic din baza de date de 20 de milioane
                grup_curent = set(random.sample(toate_numerele_ruleta, 18))

                # Calculăm întârzierea CURENTĂ (câte tururi au trecut de la ultima apariție a grupului)
                # Scanăm istoricul de la sfârșit (cel mai recent număr) spre început (cel mai vechi)
                intarziere_curenta = 0
                pentru_afisare = True

                for numar in reversed(istoric):
                    if numar in grup_curent:
                        break
                    else:
                        intarziere_curenta += 1

                if intarziere_curenta > cea_mai_mare_intarziere:
                    cea_mai_mare_intarziere = intarziere_curenta

                # Dacă acest grup are o întârziere activă exact acum de minim 22 de tururi, îl salvăm
                if intarziere_curenta >= 22 and len(grupuri_in_pinda_gasite) < 3:
                    if grup_curent not in [g[0] for g in grupuri_in_pinda_gasite]:
                        grupuri_in_pinda_gasite.append((grup_curent, intarziere_curenta))

            # Actualizare ecran
            procent = min(((batch + 1) * BATCH_SIZE) / total_grupuri_tinta, 1.0)
            progress_bar.progress(procent)
            status_text.text(f"Scanat {int(procent*100)}% din cele 20M de grupuri...")

        durata_totala = time.time() - timp_start
        progress_bar.progress(1.0)
        status_text.text("Scanare finalizată!")

        # --- AFIȘARE ALERTE ȘI REZULTATE ---
        st.success(f"### Scannere finalizat în {durata_totala:.2f} secunde")
        st.metric("Cea mai mare întârziere activă găsită", f"{cea_mai_mare_intarziere} tururi")

        if grupuri_in_pinda_gasite:
            st.error("🚨 ALERȚĂ: AU FOST GĂSITE GRUPURI PREGĂTITE PENTRU PARIERE!")
            for idx, (grup, intarziere) in enumerate(grupuri_in_pinda_gasite, 1):
                st.write(f"**Grupul sugerat #{idx} (Întârziere actuală: {intarziere} tururi):**")
                st.code(str(sorted(list(grup))))
                st.write("👉 *Miza recomandată: Pariază pe aceste 18 numere.*")
        else:
            st.info("ℹ️ Niciun grup din cele 20 de milioane nu a atins încă pragul critic de 22 de tururi de absență continuă. Mai introdu numere.")


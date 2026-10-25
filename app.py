import random
import time
import streamlit as st

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(page_title="Roulette Normal 20M 1H Secure", page_icon="🎰", layout="centered")

# --- CONFIGURARE PAROLĂ ---
PAROLA_CORECTA = "Ruleta2026"  # <-- Schimbă textul dintre ghilimele cu parola dorită de tine

# Inițializăm starea sesiunii pentru parolă dacă nu există
if "autentificat" not in st.session_state:
    st.session_state["autentificat"] = False

# --- ECRAN DE AUTENTIFICARE ---
if not st.session_state["autentificat"]:
    st.title("🔒 Acces Restricționat")
    parola_introdusa = st.text_input("Introdu parola pentru a accesa softul:", type="password")

    if st.button("Conectare", use_container_width=True):
        if parola_introdusa == PAROLA_CORECTA:
            st.session_state["autentificat"] = True
            st.rerun()  # Reîncărcăm pagina pentru a afișa softul
        else:
            st.error("Parolă incorectă! Încearcă din nou.")
    st.stop()  # Oprim execuția restului paginii dacă utilizatorul nu este logat

# --- CODUL APLICAȚIEI (Se execută doar dacă este autentificat) ---
st.title("🎰 Simulator Ruletă - 20 Milioane Tururi (Securizat)")
st.write("Monitorizează grupuri de 18 numere cu ZERO normal. Timp limită extins la **60 de minute**. Pândă la **22 de tururi**.")

# Buton de deconectare în partea de sus
if st.button("🔓 Deconectare", type="secondary"):
    st.session_state["autentificat"] = False
    st.rerun()

st.divider()

# --- MENIURI ȘI CONFIGURARE ---
timp_limita_minute = st.slider("Timp limită oprire (minute):", min_value=1, max_value=60, value=60)
total_spins = 20_000_000
PANDA_THRESHOLD = 22
MAX_TIME_SECONDS = timp_limita_minute * 60

# --- GENERARE AUTOMATĂ GRUPURI NATURALE ---
toate_numerele = list(range(0, 37))
random.seed(999)

grupuri_aleatorii = {}
for i in range(1, 6):
    numere_grup = random.sample(toate_numerele, 18)
    grupuri_aleatorii[f"Grup Aleatoriu #{i}"] = set(numere_grup)

# --- AFIȘARE COMPONEȚĂ GRUPURI ---
with st.expander("👁️ Vezi numerele din fiecare grup (observă cum 0 apare doar natural)"):
    for nume, numere in grupuri_aleatorii.items():
        are_zero = "(Conține 0)" if 0 in numere else "(NU conține 0)"
        st.write(f"**{nume}** {are_zero}: {sorted(list(numere))}")

# --- INIȚIALIZARE VECTORI ---
streaks_curente = {nume: 0 for nume in grupuri_aleatorii}
pande_reusite = {nume: 0 for nume in grupuri_aleatorii}
streaks_maxime = {nume: 0 for nume in grupuri_aleatorii}

# --- BUTON PORNIRE ---
if st.button("🚀 PORNEȘTE SIMULAREA PE TELEFON", use_container_width=True):
    spins_executate = 0
    status_text = st.empty()
    progress_bar = st.progress(0)

    timp_start = time.time()
    mod_oprire = "Toate cele 20.000.000 de tururi au fost procesate"

    # --- BUCLA PRINCIPALĂ ---
    for i in range(total_spins):
        spins_executate += 1

        # Verificare timp la fiecare 500.000 de tururi pentru viteză maximă în cloud
        if spins_executate % 500_000 == 0:
            durata_acumulata = time.time() - timp_start
            procent = min(spins_executate / total_spins, 1.0)
            progress_bar.progress(procent)
            status_text.text(f"Progres: {spins_executate:,} / 20,000,000 tururi... ({int(durata_acumulata)}s scurs)")

            if durata_acumulata >= MAX_TIME_SECONDS:
                mod_oprire = f"Limita de timp a fost atinsă ({timp_limita_minute} min)"
                break

        # Extragerea numărului (0 - 36)
        numar_extras = random.randint(0, 36)

        # Evaluăm fiecare grup în parte
        for nume_grup, numere_grup in grupuri_aleatorii.items():
            if numar_extras in numere_grup:
                if streaks_curente[nume_grup] >= PANDA_THRESHOLD:
                    pande_reusite[nume_grup] += 1
                streaks_curente[nume_grup] = 0 
            else:
                streaks_curente[nume_grup] += 1
                if streaks_curente[nume_grup] > streaks_maxime[nume_grup]:
                    streaks_maxime[nume_grup] = streaks_curente[nume_grup]

    durata_totala = time.time() - timp_start
    progress_bar.progress(1.0)
    status_text.text("Simulare finalizată!")

    # --- RAPORT VIZUAL ---
    st.success("### Rezultate Statistice Ruletă")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Tururi Rulate", f"{spins_executate:,}")
    with col2:
        st.metric("Timp de Calcul Cloud", f"{durata_totala:.2f} secunde")

    st.info(f"**Condiție oprire:** {mod_oprire}")

    # Tabel curat, optimizat pentru ecranul telefonului
    st.write("### Performanța grupurilor normale de 18 numere:")
    tabel_date = []
    for nume_grup in grupuri_aleatorii:
        tabel_date.append({
            "Nume Grup": nume_grup,
            "Pânde Prinse (Întârziere ≥ 22)": f"{pande_reusite[nume_grup]:,} ori",
            "Întârzierea Maximă (Tururi)": streaks_maxime[nume_grup]
        })

    st.table(tabel_date)


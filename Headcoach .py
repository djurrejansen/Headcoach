import streamlit as st
import random

st.set_page_config(page_title="HeadCoach - Hockey Opstellingmaker", layout="centered")

st.title("🏑 HeadCoach - Slimme Opstellingmaker voor Hockey")
st.markdown("Vul hieronder je team in voor een 8- of 11-tal en genereer automatisch een opstelling en wisselplan.")

# Teamgrootte kiezen
teamformaat = st.selectbox("Welk teamformaat wil je gebruiken?", [8, 11])

# Positie-opties
posities = [
    "Keeper",
    "Allround Verdediger",
    "Allround Middenvelder",
    "Allround Aanvaller",
    "Laatste Man",
    "Voorstopper",
    "Links Achter",
    "Rechts Achter",
    "Links Midden",
    "Rechts Midden",
    "Links Voor",
    "Rechts Voor",
    "Spits",
    "Mid Mid"
]

speelsterkte_opties = ["*", "**", "***", "****", "*****"]
aanwezigheid_opties = ["Aanwezig", "Afwezig"]

# Spelersinvoer
st.markdown("### 👥 Spelersinvulling")
spelers = []
for i in range(1, 23):
    col1, col2, col3, col4 = st.columns([3, 3, 2, 2])
    with col1:
        naam = st.text_input(f"Speler {i} - Naam", key=f"naam_{i}")
    with col2:
        positie = st.selectbox("Positie", posities, key=f"positie_{i}")
    with col3:
        sterkte = st.selectbox("Speelsterkte", speelsterkte_opties, key=f"sterkte_{i}")
    with col4:
        aanwezig = st.selectbox("Aanwezigheid", aanwezigheid_opties, key=f"aanwezig_{i}")

    if naam:
        spelers.append({
            "naam": naam,
            "positie": positie,
            "sterkte": sterkte.count("*"),
            "aanwezig": aanwezig
        })

# Opstelling genereren
if st.button("🎯 Genereer Opstelling"):
    actieve_spelers = [s for s in spelers if s['aanwezig'] == "Aanwezig"]
    actieve_spelers = sorted(actieve_spelers, key=lambda x: x['sterkte'], reverse=True)

    opstelling = []
    wissels = []

    if len(actieve_spelers) >= teamformaat:
        opstelling = actieve_spelers[:teamformaat]
        wissels = actieve_spelers[teamformaat:]
    else:
        opstelling = actieve_spelers

    st.subheader("📋 Startopstelling")
    for speler in opstelling:
        st.markdown(f"- **{speler['naam']}** ({speler['positie']}, sterkte: {'*'*speler['sterkte']})")

    if wissels:
        st.subheader("🔁 Wisselspelers")
        for speler in wissels:
            st.markdown(f"- {speler['naam']} ({speler['positie']}, sterkte: {'*'*speler['sterkte']})")

    # Simpele wisselplanning per kwart
    st.subheader("📆 Wisselplan (per kwart van 15 minuten)")
    total_blocks = 4
    blokken = {}
    wissel_ronde = wissels.copy()
    wissel_index = 0

    for i in range(1, total_blocks + 1):
        block_key = f"Kwart {i}"
        block_players = opstelling.copy()
        if wissel_ronde:
            wisselspeler = wissel_ronde[wissel_index % len(wissel_ronde)]
            gewisselde_speler = block_players[-1]
            block_players[-1] = wisselspeler
            blokken[block_key] = {
                "in": wisselspeler['naam'],
                "uit": gewisselde_speler['naam'],
                "opstelling": [p['naam'] for p in block_players]
            }
            wissel_index += 1
        else:
            blokken[block_key] = {"opstelling": [p['naam'] for p in block_players]}

    for kwart, data in blokken.items():
        st.markdown(f"**{kwart}**")
        if "in" in data:
            st.markdown(f"- Wissel: **{data['in']}** erin voor **{data['uit']}**")
        st.markdown(f"- Opstelling: {', '.join(data['opstelling'])}")
else:
    st.info("Voer spelers in en klik op 'Genereer Opstelling' om te starten.")

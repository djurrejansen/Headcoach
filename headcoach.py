
import streamlit as st
import random
from collections import defaultdict
import matplotlib.pyplot as plt

st.set_page_config(page_title="HeadCoach - Hockey Opstellingmaker", layout="centered")

st.title("🏑 HeadCoach - Slimme Opstellingmaker voor Hockey")
st.markdown("Vul hieronder je team in voor een 8- of 11-tal. De app kiest automatisch de sterkste en meest gebalanceerde opstelling zonder overlap in posities.")

# Teamgrootte kiezen
teamformaat = st.selectbox("Welk teamformaat wil je gebruiken?", [8, 11])

# Positie-opties (voorkeur)
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
        positie = st.selectbox("Voorkeurspositie", posities, key=f"positie_{i}")
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

# Definitieve posities voor 8- en 11-tallen
vaste_posities = {
    8: ["Keeper", "Laatste Man", "Voorstopper", "Links Midden", "Rechts Midden", "Links Voor", "Rechts Voor", "Spits"],
    11: ["Keeper", "Links Achter", "Rechts Achter", "Laatste Man", "Voorstopper", "Links Midden", "Rechts Midden", "Mid Mid", "Links Voor", "Rechts Voor", "Spits"]
}

positie_coords = {
    "Keeper": (5, 30),
    "Links Achter": (20, 45),
    "Rechts Achter": (20, 15),
    "Laatste Man": (20, 30),
    "Voorstopper": (30, 30),
    "Links Midden": (45, 45),
    "Rechts Midden": (45, 15),
    "Mid Mid": (45, 30),
    "Links Voor": (70, 45),
    "Rechts Voor": (70, 15),
    "Spits": (80, 30)
}

if st.button("🎯 Genereer Opstelling"):
    actieve_spelers = [s for s in spelers if s['aanwezig'] == "Aanwezig"]
    actieve_spelers = sorted(actieve_spelers, key=lambda x: x['sterkte'], reverse=True)
    beschikbare_posities = vaste_posities[teamformaat].copy()
    opstelling = []
    wissels = []

    toegewezen_posities = set()

    for speler in actieve_spelers:
        voorkeur = speler['positie']
        toegewezen = None
        if voorkeur in beschikbare_posities:
            toegewezen = voorkeur
        else:
            alternatieven = [p for p in beschikbare_posities if p not in toegewezen_posities]
            if alternatieven:
                toegewezen = alternatieven[0]

        if toegewezen:
            speler['definitieve_positie'] = toegewezen
            opstelling.append(speler)
            toegewezen_posities.add(toegewezen)
            beschikbare_posities.remove(toegewezen)
        else:
            wissels.append(speler)

    st.subheader("📋 Startopstelling (sterkste team op unieke posities)")
    for speler in opstelling:
        st.markdown(f"- **{speler['naam']}** – {speler['definitieve_positie']} (sterkte: {'*'*speler['sterkte']})")

    if wissels:
        st.subheader("🔁 Wisselspelers")
        for speler in wissels:
            st.markdown(f"- {speler['naam']} ({speler['positie']}, sterkte: {'*'*speler['sterkte']})")

    # Wisselplan per kwart (evenredig)
    st.subheader("📆 Wisselplan (4 kwarten van 15 minuten)")
    total_blocks = 4
    rotatieschema = defaultdict(list)
    full_team = opstelling + wissels
    spelers_per_blok = teamformaat
    teller = 0

    for i in range(1, total_blocks + 1):
        block_key = f"Kwart {i}"
        geselecteerd = sorted(full_team, key=lambda x: x['sterkte'], reverse=True)
        rotatie = geselecteerd[teller:teller + spelers_per_blok]
        if len(rotatie) < spelers_per_blok:
            rotatie += geselecteerd[0:spelers_per_blok - len(rotatie)]
        teller += spelers_per_blok
        if teller >= len(full_team):
            teller = 0
        rotatieschema[block_key] = rotatie

    for blok, groep in rotatieschema.items():
        st.markdown(f"**{blok}**")
        for speler in groep:
            st.markdown(f"- {speler['naam']} – {speler.get('definitieve_positie', speler['positie'])} (sterkte: {'*'*speler['sterkte']})")

    # Visualisatie veld met opstelling
    st.subheader("🟢 Visuele opstelling op het veld")
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.set_facecolor("#a8f0a5")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Bovenaanzicht hockeyveld - Positiespelers")

    # Veldlijnen
    ax.plot([50, 50], [0, 60], color="white", linestyle="--")
    ax.plot([0, 100], [0, 0], color="white")
    ax.plot([0, 100], [60, 60], color="white")

    for speler in opstelling:
        pos = speler.get("definitieve_positie")
        x, y = positie_coords.get(pos, (0, 0))
        ax.plot(x, y, 'ro')
        ax.text(x + 1, y + 1, speler['naam'], fontsize=9, color='black')

    st.pyplot(fig)
else:
    st.info("Voer spelers in en klik op 'Genereer Opstelling' om te starten.")

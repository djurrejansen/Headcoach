
import streamlit as st
import matplotlib.pyplot as plt
from collections import defaultdict

st.set_page_config(page_title="HeadCoach - Hockey Opstellingmaker", layout="centered")

st.title("🏑 HeadCoach - Slimme Opstellingmaker voor Hockey")
st.markdown("Kies je team, vul je spelers in, en genereer automatisch de sterkste opstelling met eerlijke speeltijd en visuele weergave.")

# Teamformaat kiezen
teamformaat = st.selectbox("Teamformaat", [8, 11])

# Posities
posities = [
    "Keeper", "Allround Verdediger", "Allround Middenvelder", "Allround Aanvaller",
    "Laatste Man", "Voorstopper", "Links Achter", "Rechts Achter",
    "Links Midden", "Rechts Midden", "Links Voor", "Rechts Voor",
    "Spits", "Mid Mid"
]

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

speelsterkte_opties = ["*", "**", "***", "****", "*****"]
aanwezigheid_opties = ["Aanwezig", "Afwezig"]

# Spelersinvoer
spelers = []
st.markdown("### 👥 Spelersinvoer")
for i in range(1, 23):
    cols = st.columns([3, 3, 2, 2])
    naam = cols[0].text_input(f"Naam speler {i}", key=f"naam_{i}")
    positie = cols[1].selectbox("Voorkeurspositie", posities, key=f"positie_{i}")
    sterkte = cols[2].selectbox("Sterkte", speelsterkte_opties, key=f"sterkte_{i}").count("*")
    aanwezig = cols[3].selectbox("Aanwezigheid", aanwezigheid_opties, key=f"aanwezig_{i}")
    if naam:
        spelers.append({
            "naam": naam,
            "positie": positie,
            "sterkte": sterkte,
            "aanwezig": aanwezig
        })

if st.button("🎯 Genereer Opstelling"):
    # Filter op aanwezigen
    aanwezig_spelers = [s for s in spelers if s["aanwezig"] == "Aanwezig"]
    aanwezig_spelers.sort(key=lambda x: x["sterkte"], reverse=True)

    gekozen_posities = set()
    opstelling = []
    wissels = []

    beschikbare_posities = vaste_posities[teamformaat][:]

    for speler in aanwezig_spelers:
        voorkeurspositie = speler["positie"]
        toegewezen = None
        if voorkeurspositie in beschikbare_posities:
            toegewezen = voorkeurspositie
        else:
            for pos in beschikbare_posities:
                if pos not in gekozen_posities:
                    toegewezen = pos
                    break
        if toegewezen:
            speler["definitieve_positie"] = toegewezen
            opstelling.append(speler)
            gekozen_posities.add(toegewezen)
            beschikbare_posities.remove(toegewezen)
        else:
            wissels.append(speler)

    st.subheader("📋 Startopstelling")
    for s in opstelling:
        st.markdown(f"- **{s['naam']}** – {s['definitieve_positie']} ({'*'*s['sterkte']})")

    if wissels:
        st.subheader("🔁 Wisselspelers")
        for w in wissels:
            st.markdown(f"- {w['naam']} – {w['positie']} ({'*'*w['sterkte']})")

    st.subheader("📆 Wisselplan")
    schema = defaultdict(list)
    total_blocks = 4
    full_team = opstelling + wissels
    spelers_per_blok = teamformaat
    teller = 0
    for kwart in range(1, total_blocks + 1):
        geselecteerd = full_team[teller:teller+spelers_per_blok]
        if len(geselecteerd) < spelers_per_blok:
            geselecteerd += full_team[0:spelers_per_blok - len(geselecteerd)]
        schema[f"Kwart {kwart}"] = geselecteerd
        teller = (teller + spelers_per_blok) % len(full_team)

    for kwart, groep in schema.items():
        st.markdown(f"**{kwart}**")
        for s in groep:
            st.markdown(f"- {s['naam']} ({s.get('definitieve_positie', s['positie'])}, {'*'*s['sterkte']})")

    # Visualisatie veld
    st.subheader("🟢 Visuele Opstelling")
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.set_facecolor("#a8f0a5")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Bovenaanzicht hockeyveld")

    # Lijnen
    ax.plot([50, 50], [0, 60], color="white", linestyle="--")
    ax.plot([0, 100], [0, 0], color="white")
    ax.plot([0, 100], [60, 60], color="white")

    for speler in opstelling:
        pos = speler.get("definitieve_positie")
        if pos in positie_coords:
            x, y = positie_coords[pos]
            ax.plot(x, y, 'ro')
            ax.text(x + 1, y + 1, speler["naam"], fontsize=9)

    st.pyplot(fig)
else:
    st.info("Vul je team in en klik op 'Genereer Opstelling'.")

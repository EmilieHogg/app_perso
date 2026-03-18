import streamlit as st
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import re
import json
from streamlit_lottie import st_lottie
import time
import feedparser
import urllib.request

# ── Page config ────────────────────────────────────────────
st.set_page_config(page_title="Tableau de bord interactif", layout="centered")

# ── Sidebar Navigation ─────────────────────────────────────
page = st.sidebar.radio("Navigation", ["Accueil", "Meteo", "Operas de Paris", "Valeurs du CAC40", "Actualite"])

# ── Load lottie animation ──────────────────────────────────
def load_lottiefile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_confetti = load_lottiefile("confetti.json")

# ══════════════════════════════════════════════════════════
# PAGE ACCUEIL
# ══════════════════════════════════════════════════════════
def show_accueil():
    placeholder = st.empty()
    with placeholder.container():
        st_lottie(lottie_confetti, speed=1, loop=False)
    time.sleep(2.5)
    with placeholder.container():
        st.markdown("""
            <style>
            .fade-in {
                animation: fadeIn 2s ease-in;
                text-align: center;
            }
            @keyframes fadeIn {
                0% {opacity:0; transform: translateY(20px);}
                100% {opacity:1; transform: translateY(0);}
            }
            </style>
            <div class="fade-in">
                <h1>Bonjour Jean-Pol</h1>
                <h3>Bienvenue sur ton <span style="color:#ff4b4b;">tableau de bord interactif</span> !</h3>
            </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGE METEO
# ══════════════════════════════════════════════════════════
def show_meteo():
    st.title("Meteo")
    cities = ["Paris", "Andernos-les-Bains"]
    api_key = "e8908a3217f223d1a784c8a38643e51f"

    for city in cities:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": "metric", "lang": "fr"}
        try:
            r = requests.get(url, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
            temp = data["main"]["temp"]
            icon = data["weather"][0]["icon"]
            st.markdown(f"### {city}")
            st.image(f"https://openweathermap.org/img/wn/{icon}@2x.png", width=80)
            st.metric(label="Temperature", value=f"{temp} C")
        except Exception as e:
            st.error(f"Erreur meteo pour {city} : {e}")

# ══════════════════════════════════════════════════════════
# PAGE OPERA — no Selenium, hardcoded shows + direct links
# ══════════════════════════════════════════════════════════
def show_opera():
    st.title("Opera de Paris - Saison 25/26")

    opera_shows = [
        {
            "title": "Aida",
            "dates": "24 sept. au 04 nov. 2025",
            "location": "Opera Bastille",
            "url": "https://www.operadeparis.fr/saison-25-26/opera/aida"
        },
        {
            "title": "La Walkyrie",
            "dates": "11 nov. au 30 nov. 2025",
            "location": "Opera Bastille",
            "url": "https://www.operadeparis.fr/saison-25-26/opera/la-walkyrie"
        },
        {
            "title": "Siegfried",
            "dates": "17 janv. au 31 janv. 2026",
            "location": "Opera Bastille",
            "url": "https://www.operadeparis.fr/saison-25-26/opera/siegfried"
        },
        {
            "title": "Eugene Oneguine",
            "dates": "15 nov. 2025 au 27 dec. 2025",
            "location": "Palais Garnier",
            "url": "https://www.operadeparis.fr/saison-25-26/opera/eugene-oneguine"
        },
        {
            "title": "Tosca",
            "dates": "07 fevr. au 19 mars 2026",
            "location": "Opera Bastille",
            "url": "https://www.operadeparis.fr/saison-25-26/opera/tosca"
        },
        {
            "title": "Carmen",
            "dates": "24 fevr. au 20 mars 2026",
            "location": "Opera Bastille",
            "url": "https://www.operadeparis.fr/saison-25-26/opera/carmen"
        },
        {
            "title": "Ercole Amante",
            "dates": "28 mai au 14 juin 2026",
            "location": "Opera Bastille",
            "url": "https://www.operadeparis.fr/saison-25-26/opera/ercole-amante"
        },
    ]

    ballet_shows = [
        {
            "title": "Giselle",
            "dates": "28 sept. au 31 oct. 2025",
            "location": "Palais Garnier",
            "url": "https://www.operadeparis.fr/saison-25-26/ballet/giselle"
        },
        {
            "title": "Racines",
            "dates": "06 oct. au 10 nov. 2025",
            "location": "Opera Bastille",
            "url": "https://www.operadeparis.fr/saison-25-26/ballet/racines"
        },
        {
            "title": "Notre-Dame de Paris",
            "dates": "06 dec. au 31 dec. 2025",
            "location": "Opera Bastille",
            "url": "https://www.operadeparis.fr/saison-25-26/ballet/notre-dame-de-paris"
        },
        {
            "title": "Contrastes",
            "dates": "01 dec. au 31 dec. 2025",
            "location": "Palais Garnier",
            "url": "https://www.operadeparis.fr/saison-25-26/ballet/contrastes"
        },
        {
            "title": "Le Parc",
            "dates": "03 fevr. au 25 fevr. 2026",
            "location": "Palais Garnier",
            "url": "https://www.operadeparis.fr/saison-25-26/ballet/le-parc"
        },
        {
            "title": "Empreintes",
            "dates": "11 mars au 28 mars 2026",
            "location": "Palais Garnier",
            "url": "https://www.operadeparis.fr/saison-25-26/ballet/empreintes"
        },
        {
            "title": "Romeo et Juliette",
            "dates": "02 avr. au 12 mai 2026",
            "location": "Opera Bastille",
            "url": "https://www.operadeparis.fr/saison-25-26/ballet/romeo-et-juliette"
        },
        {
            "title": "La Dame aux camelias",
            "dates": "05 mai au 23 mai 2026",
            "location": "Palais Garnier",
            "url": "https://www.operadeparis.fr/saison-25-26/ballet/la-dame-aux-camelias"
        },
        {
            "title": "La Bayadere",
            "dates": "17 juin au 14 juil. 2026",
            "location": "Opera Bastille",
            "url": "https://www.operadeparis.fr/saison-25-26/ballet/la-bayadere"
        },
        {
            "title": "Vibrations",
            "dates": "27 juin au 14 juil. 2026",
            "location": "Palais Garnier",
            "url": "https://www.operadeparis.fr/saison-25-26/ballet/vibrations"
        },
    ]

    def display_shows(shows):
        for show in shows:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"### {show['title']}")
            with col2:
                st.write(f"Dates : {show['dates']}")
                st.write(f"Lieu : {show['location']}")
            with col3:
                st.markdown(f"[Reserver]({show['url']})")
            st.divider()

    tab1, tab2 = st.tabs(["Opera", "Ballet"])
    with tab1:
        display_shows(opera_shows)
    with tab2:
        display_shows(ballet_shows)

    st.markdown("---")
    st.markdown("[Voir le programme complet](https://www.operadeparis.fr/programmation/saison-25-26)")


# ══════════════════════════════════════════════════════════
# PAGE CAC40
# ══════════════════════════════════════════════════════════
def show_cac40():
    st.title("CAC 40 Dashboard")
    filename = "CAC40_closing_prices_named.csv"
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base_dir = os.getcwd()

    file_path = os.path.join(base_dir, filename)

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Fichier non trouve : {file_path}")
        return

    CAC40_df = df.set_index("Date").apply(pd.to_numeric, errors="coerce")
    companies = CAC40_df.columns.tolist()
    selected = st.selectbox("Selectionner une societe", companies)

    prices = CAC40_df[selected].dropna()
    latest = prices.iloc[-1]

    variation_1d = latest - prices.iloc[-2]  if len(prices) > 1  else 0
    variation_1w = latest - prices.iloc[-6]  if len(prices) > 5  else 0
    variation_1m = latest - prices.iloc[-21] if len(prices) > 20 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Variation 1 jour",    f"{variation_1d:+.2f} EUR", delta=f"{variation_1d:+.2f}")
    col2.metric("Variation 1 semaine", f"{variation_1w:+.2f} EUR", delta=f"{variation_1w:+.2f}")
    col3.metric("Variation 1 mois",    f"{variation_1m:+.2f} EUR", delta=f"{variation_1m:+.2f}")

    st.subheader(f"{selected} - Historique des prix")
    st.line_chart(prices)

# ══════════════════════════════════════════════════════════
# PAGE NEWS
# ══════════════════════════════════════════════════════════
def show_news():
    st.title("Actualites - Andernos-les-Bains")

    feeds = [
        {"name": "InfoBassin",    "url": "https://www.infobassin.com/tag/andernos/feed/"},
        {"name": "TVBA Arcachon", "url": "https://tvba.fr/feed/"},
        {"name": "France Bleu",   "url": "https://www.francebleu.fr/rss/infos.xml"},
    ]

    for feed in feeds:
        st.subheader(feed["name"])
        try:
            req = urllib.request.Request(
                feed["url"],
                headers={"User-Agent": "Mozilla/5.0"}
            )
            response = urllib.request.urlopen(req, timeout=10)
            raw = response.read()
            parsed = feedparser.parse(raw)

            if not parsed.entries:
                st.warning("Aucun article trouve.")
                continue

            for entry in parsed.entries[:4]:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{entry.get('title', 'Sans titre')}**")
                    summary = entry.get("summary", "")
                    if summary:
                        clean = BeautifulSoup(summary, "html.parser").get_text()
                        st.caption(clean[:200] + "..." if len(clean) > 200 else clean)
                with col2:
                    published = entry.get("published", "")
                    if published:
                        st.caption(published[:16])
                    link = entry.get("link", "")
                    if link:
                        st.markdown(f"[Lire]({link})")
                st.divider()

        except Exception as e:
            st.error(f"Erreur : {e}")

# ══════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════
if page == "Accueil":
    show_accueil()
elif page == "Meteo":
    show_meteo()
elif page == "Operas de Paris":
    show_opera()
elif page == "Valeurs du CAC40":
    show_cac40()
elif page == "Actualite":
    show_news()
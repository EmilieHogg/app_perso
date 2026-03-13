# third_app_perso.py

import streamlit as st
import pandas as pd
import os
import time
import json
from streamlit_lottie import st_lottie
import requests
import feedparser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re

# ── Page config ───────────────────────────
st.set_page_config(page_title="Tableau de bord interactif", layout="wide")

# ── Placeholder principal ─────────────────
main_placeholder = st.empty()

# ── Fonction pour charger animation Lottie ──
def load_lottiefile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# ── Fonction pour afficher le dashboard CAC40 ──
def show_cac40_dashboard(placeholder):
    filename = "CAC40_closing_prices_named.csv"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        placeholder.error(f"❌ File not found: {file_path}")
        return

    CAC40_df = df.set_index("Date").apply(pd.to_numeric, errors='coerce')
    company_names = CAC40_df.columns.tolist()

    if not company_names:
        placeholder.error("❌ No companies found in CSV.")
        return

    with placeholder.container():
        st.sidebar.title("📊 CAC 40 Dashboard")
        selected_company = st.sidebar.selectbox("Select a company", company_names)

        st.title("CAC 40 Closing Prices")
        latest_price = CAC40_df[selected_company].dropna().iloc[-1]
        st.metric(label=f"{selected_company} — Latest Close", value=f"{latest_price:.2f} €")

        st.subheader(f"{selected_company} — Price History")
        st.line_chart(CAC40_df[selected_company])

# ── Fonction pour afficher météo, news et Opéra ──
def show_main_dashboard(placeholder):
    # 1️⃣ Confetti et message de bienvenue
    lottie_confetti = load_lottiefile("confetti.json")
    with placeholder.container():
        st_lottie(lottie_confetti, speed=1, loop=False)
    time.sleep(2.5)
    with placeholder.container():
        st.markdown("""
            <style>
            .fade-in { animation: fadeIn 2s ease-in; text-align: center; }
            @keyframes fadeIn { 0% {opacity:0; transform: translateY(20px);} 100% {opacity:1; transform: translateY(0);} }
            </style>
            <div class="fade-in">
                <h1>Bonjour Jean-Pol 👋</h1>
                <h3>Bienvenue sur ton <span style="color:#ff4b4b;">tableau de bord interactif</span> !</h3>
            </div>
        """, unsafe_allow_html=True)

    # 2️⃣ Météo
    api_key = "e8908a3217f223d1a784c8a38643e51f"
    cities = ["Paris", "Andernos-les-Bains"]

    def get_weather(city):
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": "metric", "lang": "fr"}
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        return {"city": city, "temp": data["main"]["temp"], "icon": data["weather"][0]["icon"]}

    with placeholder.container():
        st.markdown("<h2 style='text-align:center; margin-bottom:30px;'>🌤️ Météo par ville</h2>", unsafe_allow_html=True)
        cols = st.columns(len(cities))
        for i, city in enumerate(cities):
            weather = get_weather(city)
            with cols[i]:
                st.markdown(f"<h3 style='text-align:center'>{weather['city']}</h3>", unsafe_allow_html=True)
                st.image(f"https://openweathermap.org/img/wn/{weather['icon']}@2x.png", width=80)
                st.metric(label="Température", value=f"{weather['temp']} °C")

    # 3️⃣ News Courbevoie
    st.header("📰 Nouveautés – Courbevoie")
    rss_url = "https://www.actu.fr/rss/hauts-de-seine/courbevoie.xml"
    feed = feedparser.parse(rss_url)
    if feed.entries:
        for entry in feed.entries[:5]:
            st.markdown(f"<h3 style='text-align:center'>{entry.title}</h3>", unsafe_allow_html=True)
            if getattr(entry, "summary", None):
                st.write(entry.summary)
            st.markdown(f"<p style='text-align:center'><a href='{entry.link}' target='_blank'>Lire la suite</a></p>", unsafe_allow_html=True)
            st.divider()
    else:
        st.write("Pas de news récentes pour Courbevoie pour le moment.")

    # 4️⃣ Opéra de Paris (simplifié)
    st.subheader("🎭 Programmation Opéra de Paris – Saison 25/26")
    st.write("Contenu Opéra ici...")

# ── Sidebar buttons ─────────────────────────
if st.sidebar.button("Show CAC40 Dashboard"):
    main_placeholder.empty()  # vide le contenu existant
    show_cac40_dashboard(main_placeholder)
else:
    main_placeholder.empty()
    show_main_dashboard(main_placeholder)
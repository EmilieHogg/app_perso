import streamlit as st
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import re
import json
from streamlit_lottie import st_lottie
import time
import feedparser

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless=new")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


st.set_page_config(page_title="Tableau de bord interactif", layout="centered")

# ── Sidebar Navigation ─────────
page = st.sidebar.radio("Navigation", ["Accueil", "Météo", "Opéras de Paris", "Valeurs du CAC40", "Actualité"])


#from pyicloud import PyiCloudService
#import streamlit as st

#api = PyiCloudService("Yellowbanane3", "Yellowbanane3")
#photos = api.photos.all

#for photo in photos[:3]:  # show latest 3
    #st.image(photo.download().raw, use_column_width=True)

# ── Load lottie animation ─────────
def load_lottiefile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_confetti = load_lottiefile("confetti.json")


# ── Page Accueil ─────────
def show_accueil():
    placeholder = st.empty()
    # Confetti
    with placeholder.container():
        st_lottie(lottie_confetti, speed=1, loop=False)
    time.sleep(2.5)

    # Message de bienvenue
    with placeholder.container():
        st.markdown(
            """
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
                <h1>Bonjour Jean-Pol 👋</h1>
                <h3>Bienvenue sur ton <span style="color:#ff4b4b;">tableau de bord interactif</span> !</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

# ── Page Météo ─────────
def show_meteo():
    st.title("🌤️ Météo")
    cities = ["Paris", "Andernos-les-Bains"]
    api_key = "e8908a3217f223d1a784c8a38643e51f"

    for city in cities:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": "metric", "lang": "fr"}
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        temp = data["main"]["temp"]
        icon = data["weather"][0]["icon"]

        st.markdown(f"### {city}")
        st.image(f"https://openweathermap.org/img/wn/{icon}@2x.png", width=80)
        st.metric(label="Température", value=f"{temp} °C")

# ── Page Opéra ─────────
def show_opera():
    st.title("🎭 Programmation Opéra de Paris – Saison 25/26")
    programming = ["opera", "ballet"]
    base_url = "https://www.operadeparis.fr/programmation/saison-25-26"
    programming_urls = [f"{base_url}/{p}" for p in programming]

    st.write("Chargement des spectacles...")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    events = []

    try:
        for url in programming_urls:
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "li.show"))
                )
            except TimeoutException:
                continue

            soup = BeautifulSoup(driver.page_source, "html.parser")
            for show in soup.find_all("li", class_="show"):
                raw_text = show.get_text(separator=" ", strip=True)
                # Dates
                patterns = [
                    r"(du\s+\d{1,2}\s*(?:janv\.|févr\.|mars|avr\.|mai|juin|juil\.|août|sept\.|oct\.|nov\.|déc\.)\s*au\s*\d{1,2}\s*(?:janv\.|févr\.|mars|avr\.|mai|juin|juil\.|août|sept\.|oct\.|nov\.|déc\.)\s*\d{4})",
                    r"(du\s+\d{1,2}\s*au\s*\d{1,2}\s*(?:janv\.|févr\.|mars|avr\.|mai|juin|juil\.|août|sept\.|oct\.|nov\.|déc\.)\s*\d{4})",
                    r"(le\s+\d{1,2}\s*(?:janv\.|févr\.|mars|avr\.|mai|juin|juil\.|août|sept\.|oct\.|nov\.|déc\.)\s*\d{4}(?:\s+à\s*\d{1,2}h\d{2})?)"
                ]
                matches = []
                for p in patterns:
                    matches += re.findall(p, raw_text)
                dates = " ; ".join(matches) if matches else "Unknown"

                # Lieu
                location = ("Bobigny" if "Bobigny" in raw_text else
                            "Philharmonie de Paris" if "Philharmonie de Paris" in raw_text else
                            "Studio Bastille" if "Studio Bastille" in raw_text else
                            "Palais Garnier" if "Palais Garnier" in raw_text else
                            "Opéra Bastille" if "Opéra Bastille" in raw_text else
                            "Amphithéâtre" if "Amphithéâtre" in raw_text else
                            "Unknown")

                title = raw_text
                for part in [dates, location, "Voir les disponibilités", "Réserver"]:
                    if part != "Unknown":
                        title = title.replace(part, "").strip()

                link = show.find("a", href=True)
                link_url = link["href"] if link else None

                events.append({"title": title, "dates": dates, "location": location, "url": link_url})

    except WebDriverException as e:
        st.error(f"Selenium failed: {e}")
    finally:
        driver.quit()

    for e in events:
        st.markdown(f"### {e['title']}")
        st.write(f"📅 Dates : {e['dates']}")
        st.write(f"📍 Lieu : {e['location']}")
        if e["url"]:
            st.markdown(f"[🔗 Voir le spectacle]({e['url']})")
        st.divider()

# ── Page CAC40 ─────────
def show_cac40():
    st.title("📊 CAC 40 Dashboard")
    filename = "CAC40_closing_prices_named.csv"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"❌ File not found: {file_path}")
        return

    CAC40_df = df.set_index("Date").apply(pd.to_numeric, errors="coerce")
    companies = CAC40_df.columns.tolist()
    selected = st.selectbox("Sélectionner une société", companies)
    latest = CAC40_df[selected].dropna().iloc[-1]

    
    # Calcul des variations
    prices = CAC40_df[selected].dropna()

    variation_1d = latest - prices.iloc[-2] if len(prices) > 1 else 0
    variation_1w = latest - prices.iloc[-6] if len(prices) > 5 else 0
    variation_1m = latest - prices.iloc[-21] if len(prices) > 20 else 0

    # Affichage des métriques
  # Affichage des variations côte à côte
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Variation 1 jour", value=f"{variation_1d:+.2f} €")
    col2.metric(label="Variation 1 semaine", value=f"{variation_1w:+.2f} €")
    col3.metric(label="Variation 1 mois", value=f"{variation_1m:+.2f} €")

# Graphique historique
    st.subheader(f"{selected} — Historique des prix")
    st.line_chart(prices)
def show_news():
    import streamlit as st
    import requests
    from bs4 import BeautifulSoup

    st.title("📰 Actualités – Andernos")

    url = "https://www.sudouest.fr/gironde/andernos-les-bains/"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    articles = soup.select("article")[:5]

    if not articles:
        st.write("Pas de news disponibles pour Andernos.")
        return

    for a in articles:
        title = a.select_one("h2, h3")
        link = a.find("a", href=True)

        if title and link:
            st.markdown(f"### {title.text.strip()}")
            st.markdown(f"[Lire la suite]({link['href']})")
            st.divider()

# ── Affichage selon la page ─────────
if page == "Accueil":
    show_accueil()
elif page == "Météo":
    show_meteo()
elif page == "Opéras de Paris":
    show_opera()
elif page == "Valeurs du CAC40":
    show_cac40()
elif page == "Actualité":
    show_news()
import streamlit as st
import json
import time
from streamlit_lottie import st_lottie

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from PIL import Image
import streamlit.components.v1 as components
import streamlit as st
import requests

st.write("APP STARTED")

def load_lottiefile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# Load animation
lottie_confetti = load_lottiefile("confetti.json")

# Placeholder for dynamic content
placeholder = st.empty()

# 1️⃣ Show confetti first
st_lottie(lottie_confetti, speed=1, loop=False)

# Wait for confetti to play
time.sleep(2.5)  # adjust to match animation length

# 2️⃣ Show bienvenue message and keep it

with placeholder.container():
    st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <h1 style="font-size: 64px;">👋 Welcome</h1>
        <h2 style="font-size: 48px;">Bonjour Jean-Pol</h2>
        <p style="font-size: 32px; font-weight: bold;">
            Bienvenue sur ton 
            <span style="background: linear-gradient(90deg, #ff4b4b, #ffa94d, #ffd43b, #69db7c, #4dabf7);
                         -webkit-background-clip: text;
                         -webkit-text-fill-color: transparent;">
                tableau de bord interactif
            </span> !
        </p>
    </div>
    """, unsafe_allow_html=True)

'''with placeholder.container():
    st.write("👋 Welcome")
    st.title("Bonjour Jean-Pol")
    st.markdown("""
    **Bienvenue sur ton :rainbow[tableau de bord] interactif !**
    """)'''





# -------------------------------
# STREAMLIT UI
# -------------------------------







base_url = "https://www.operadeparis.fr"
programming_url = f"{base_url}/programmation/saison-25-26/"

variable_url = {"opera": "opera", "spectacles-ballet": "spectacles-ballet", "concert-et-recital": "concert-et-recital"}

for value in variable_url.values():
    programming_url = f"https://www.operadeparis.fr/programmation/saison-25-26/{value}"
    #print(programming_url)


# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

events = []


try:
    driver.get(programming_url)
    
    # Wait for event cards to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "FeaturedList__reserve-img"))
    )
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    

    cards = soup.find_all("a", class_="FeaturedList__reserve-img")
    shows = soup.find_all("li", class_="show")


    
  
    for card in cards:
        img = card.find("img")
        title = img.get("alt").strip() if img else None

    
    
    for show in shows:
        tag = show.find("a", class_="FeaturedList__reserve-img")
        img = tag.find("img") if tag else None
        title = img.get("alt").strip() if img else "N/A"
        href = tag.get("href") if tag else None
        url = base_url + href if href and href.startswith("/") else href
        dates = show.find("p", class_="show_date")
        location = show.find("p", class_="show_place")

        events.append({
        "title": title,
        "dates": dates.text.strip() if dates else "N/A",
        "location": location.text.strip() if location else "N/A",
        "url": url
    })


finally:
    driver.quit()

# Remove duplicates
unique_events = []
seen_urls = set()
for e in events:
    if e["url"] not in seen_urls:
        unique_events.append(e)
        seen_urls.add(e["url"])

# Display results

'''for e in unique_events:
    print(f"Titre  : {e['title']}")
    print(f"Dates  : {e['dates']}")
    print(f"Lieu   : {e['location']}")
    print(f"URL    : {e['url']}")
    print("-" * 40)'''

#print(f"Total événements : {len(unique_events)}")

st.subheader('Programmation Opera de Paris, saison 25/26')
st.write(f"Title : {e['title']}")
st.write(f"Dates : {e['dates']}")
                    
st.write(f"Total evenements ; {len(unique_events)}")

import pandas as pd

# Convert list of dicts to DataFrame
df_events = pd.DataFrame(unique_events)

st.subheader("🎭 Programmation Opéra de Paris – Saison 25/26")
st.write("DEBUG: reached dataframe section")
st.write(unique_events)


st.dataframe(
    df_events,
    column_config={
        "title": "Titre",
        "dates": "Dates",
        "location": "Lieu",
        "url": st.column_config.LinkColumn("Lien")
    },
    hide_index=True,
    use_container_width=True
)

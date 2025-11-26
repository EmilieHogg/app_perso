

import numpy as np
from PIL import Image
import streamlit.components.v1 as components
import streamlit as st
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd




st.write(" Welcome") 

st.image("https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif")

st.title("Bonjour Jean-Pol")
st.markdown(
    """ 
    

    **Bienvenue sur ton :rainbow[tableau de bord] interactif!**
    
    """
)

st.subheader('Programmation Opera de Paris, saison 25/26')
st.write(f"Title : {e['title']}")
st.write(f"Dates : {e['dates']}")
                    
st.write(f"Total evenements ; {len(unique_events)}")

st.balloons()


if st.button("Send balloons!"):
    st.balloons()

    from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import re

base_url = "https://www.operadeparis.fr"
programming_url = f"{base_url}/programmation/saison-25-26/opera"

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
        title = img.get("alt").strip() if img and img.get("alt") else None

    
    

    for show in shows:

        date_tag = show.find("p", class_="show_date")
        dates = date_tag.get_text(strip=True) if date_tag else None

        loc_tag = show.find("p", class_ ="show_place")
        location = loc_tag.get_text(strip=True) if loc_tag else None

        href = card.get("href")
        url = base_url + href if href and href.startswith("/") else href

        events.append({
            "title": title,
            "dates": dates,
            "location": location,
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
for e in unique_events:
    print(f"Titre  : {e['title']}")
    print(f"Dates  : {e['dates']}")
    print(f"Lieu   : {e['location']}")
    print(f"URL    : {e['url']}")
    print("-" * 40)

print(f"Total événements : {len(unique_events)}")

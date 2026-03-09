print("Script started")


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
from playwright.sync_api import sync_playwright
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import streamlit as st
import time
import re
import pandas as pd
import requests
import streamlit as st
import unicodedata

api_key = "e8908a3217f223d1a784c8a38643e51f"

cities = ["Paris", "Andernos-les-Bains"]

def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "fr"
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()

    return {
        "city": city,
        "temp": data["main"]["temp"],
        "icon": data["weather"][0]["icon"]
    }

def icon_url(icon_id):
    return f"https://openweathermap.org/img/wn/{icon_id}@2x.png"

st.title("🌤️ Météo par ville")

for city in cities:
    weather = get_weather(city)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(icon_url(weather["icon"]), width=80)
    with col2:
        st.write(f"**{weather['city']}**")
        st.write(f"{weather['temp']} °C")






st.write(" Welcome") 

st.image("https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif")

st.title("Bonjour Jean-Pol")
st.markdown(
    """ 
    

    **Bienvenue sur ton :rainbow[tableau de bord] interactif!**
    
    """
)



'''base_url = "https://www.operadeparis.fr"
programming_url = f"{base_url}/programmation/saison-25-26/opera"'''
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

programming = ["opera", "ballet"]
base_url = "https://www.operadeparis.fr/programmation/saison-25-26"
programming_urls = [f"{base_url}/{p}" for p in programming]

print(programming_urls)


def scrape_events(programming_urls):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    events = []

    # Initialize driver once
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        for url in programming_urls:
            driver.get(url)
            try:
                # Wait up to 10 seconds for at least one show
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "li.show"))
                )
            except TimeoutException:
                print(f"No shows found on {url}")
                continue  # skip to next url

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            show_elements = soup.find_all("li", class_="show")
            print(f"Found shows on {url}: {len(show_elements)}")

            for show in show_elements:
                raw_text = show.get_text(separator=" ", strip=True)
                full_dates = "Unknown"
                link_element = show.find("a", href=True)
                link = link_element["href"] if link_element else None

                  # Regex patterns for multiple date formats
                patterns = [
                    r"(du\s+\d{1,2}\s*(?:janv\.|févr\.|mars|avr\.|mai|juin|juil\.|août|sept\.|oct\.|nov\.|déc\.)\s*au\s*\d{1,2}\s*(?:janv\.|févr\.|mars|avr\.|mai|juin|juil\.|août|sept\.|oct\.|nov\.|déc\.)\s*\d{4})",
                    r"(du\s+\d{1,2}\s*au\s*\d{1,2}\s*(?:janv\.|févr\.|mars|avr\.|mai|juin|juil\.|août|sept\.|oct\.|nov\.|déc\.)\s*\d{4})",
                    r"(le\s+\d{1,2}\s*(?:janv\.|févr\.|mars|avr\.|mai|juin|juil\.|août|sept\.|oct\.|nov\.|déc\.)\s*\d{4}(?:\s+à\s*\d{1,2}h\d{2})?)"
                ]

                matches = []
                for pattern in patterns:
                    matches += re.findall(pattern, raw_text)

                if matches:
                    full_dates = " ; ".join(matches)


                # Determine location
                location = ("Bobigny" if "Bobigny" in raw_text else
                            "Philharmonie de Paris" if "Philharmonie de Paris" in raw_text else
                            "Studio Bastille" if "Studio Bastille" in raw_text else
                            "Palais Garnier" if "Palais Garnier" in raw_text else
                            "Opéra Bastille" if "Opéra Bastille" in raw_text else
                            "Amphithéâtre" if "Amphithéâtre" in raw_text else
                            "Unknown")

                # Clean title
                title = raw_text
                for part in [full_dates, location, "Voir les disponibilités", "Réserver"]:
                    if part and part != "Unknown":
                        title = title.replace(part, "").strip()

                events.append({
                    "title": title,
                    "dates": full_dates,
                    "location": location,
                    "url": link
                })

    except WebDriverException as e:
        print(f"❌ Selenium failed: {e}")

    finally:
        driver.quit()

    return events


# Scrape events
events = scrape_events(programming_urls)

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


st.subheader("🎭 Programmation Opéra de Paris – Saison 25/26")

for e in unique_events:
    st.markdown(f"### {e['title']}")
    st.write(f"📅 **Dates** : {e['dates']}")
    st.write(f"📍 **Lieu** : {e['location']}")
    st.markdown(f"[🔗 Voir le spectacle]({e['url']})")
    st.divider()

                    
st.write(f"Total evenements ; {len(unique_events)}")

st. subheader ("Valeurs du CAC 4O")



# third_app_perso.py
import streamlit as st
from CAC40 import load_cac40
import os

# File name next to the script
filename = "CAC40_closing_prices_named.csv"  # replace with your file name
script_dir = os.path.dirname(os.path.abspath("CAC40_closing_prices_named.csv"))

# Full path
file_path = os.path.join(script_dir, "CAC40_closing_prices_named.csv")

# Load into a DataFrame
df = pd.read_csv(file_path)
print(df)



CAC40_transposed_closing_price_named = df.set_index("Date").T
CAC40_transposed_closing_price_named = df.set_index("Date")
#CAC40_transposed_closing_price_named = df.T

print(CAC40_transposed_closing_price_named.head())
print(CAC40_transposed_closing_price_named.columns)
print(CAC40_transposed_closing_price_named.index)



# Streamlit selectbox for companies only
company_names = CAC40_transposed_closing_price_named.columns  # all columns are companies

selected_company = st.sidebar.selectbox(
    "Select a company",
    company_names
)

# Access last two columns dynamically
penultimate = CAC40_transposed_closing_price_named.columns[-2]
last = CAC40_transposed_closing_price_named.columns[-1]

# Convert last two columns to numeric
CAC40_transposed_closing_price_named[penultimate] = pd.to_numeric(CAC40_transposed_closing_price_named[penultimate], errors='coerce')
CAC40_transposed_closing_price_named[last] = pd.to_numeric(CAC40_transposed_closing_price_named[last], errors='coerce')


latest_price = CAC40_transposed_closing_price_named[selected_company].iloc[-1]
st.write(f"Latest price: {latest_price:.2f} €")

st.metric(
label=f"{selected_company} Latest Close",
value=f"{latest_price:.2f} €"
)
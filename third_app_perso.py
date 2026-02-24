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



import requests
import streamlit as st

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

                # Extract month & year
                month_year_match = re.search(r"(janv\.|févr\.|mars|avr\.|mai|juin|juil\.|août|sept\.|oct\.|nov\.|déc\.)\s*\d{4}", raw_text)
                month_year = month_year_match.group(0) if month_year_match else ""

                # Extract day range
                day_range_match = re.search(r"(\d{1,2}\s*au\s*\d{1,2})", raw_text)
                day_range = day_range_match.group(1) if day_range_match else ""

                if day_range and month_year:
                    full_dates = f"{day_range} {month_year}"

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
                for part in [full_dates, location, "Voir les disponibilités"]:
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

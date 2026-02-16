print("Script started")


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
from playwright.sync_api import sync_playwright
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import streamlit as st
import time



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

    for url in programming_urls:
        driver = None
        try:
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            time.sleep(3)

            html = driver.page_source  # get page HTML from Selenium driver
            soup = BeautifulSoup(html, "html.parser")  # create soup object

            show_elements = soup.find_all("li", class_="show")
            print("Found shows:", len(show_elements))

        

            for show in show_elements:
                link_element = show.find("a", class_="FeaturedList__reserve--img")
                if link_element and link_element.has_attr("href"):
                    link = link_element.get("href")
                    title = link_element.get("aria-label", link_element.text)
                else:
                    link = "Unknown"
                    title = show.get_text(strip=True)
                    
                    events.append({
                    "title": title,
                    "dates": "Unknown",
                    "location": "Unknown",
                    "url": link
                 })

            
    # For demo, fill dates/location with Unknown or extract more from show if needed
    
                    
            #for show in show_elements:
                #title = show.text
                #link = show.get_attribute("href")
                #events.append({
                    #"title": title,
                    #"dates": "Unknown",
                    #"location": "Unknown",
                    #"url": link
                #})

            print(f"Loaded {url} with {len(show_elements)} events")

        except WebDriverException as e:
            print(f"❌ Selenium failed on {url}: {e}")

        finally:
            if driver:
                driver.quit()

    return events

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

print("Script started")


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
from playwright.sync_api import sync_playwright
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


import requests

city = "Paris", "Andernos-les-bains"

api_key = "e8908a3217f223d1a784c8a38643e51f"

city = "Paris"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=fr"

response = requests.get(url)
print(response.status_code)
print(response.text)


cities = ["Andernos-les-bains", "Paris"]


print (city)

def get_weather(city):
    api_key = "e8908a3217f223d1a784c8a38643e51f"  # Free from OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=fr"
    data = requests.get(url).json()
    
    if "main" not in data:
        return {"error": data.get("message", "City not found")}
    
    return {
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "unit": "°C"}

for city in cities: 
    print (f" météo {city}:", get_weather(city))



'''with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent="Mozilla/5.0 ...")
    page.goto(f"https://www.google.com/search?q=weather+{city}", timeout=60000)
    
    page.wait_for_selector("#wob_tm", timeout=15000)
    
    html = page.content()
    browser.close()

print(html)

soup = BeautifulSoup(html, "html.parser")

temperature = soup.select_one("#wob_tm").text if soup.select_one("#wob_tm") else None
description = soup.select_one("#wob_dc").text if soup.select_one("#wob_dc") else None

print("Temperature:", temperature)
print("Description:", description)'''



#import numpy as np
#from PIL import Image
#import streamlit.components.v1 as components
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

st.balloons()


if st.button("Send balloons!"):
    st.balloons()
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# -------------------------------
# STREAMLIT UI
# -------------------------------

st.write(" Welcome")
st.image("https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif")

st.title("Bonjour Jean-Pol")
st.markdown("""
**Bienvenue sur ton :rainbow[tableau de bord] interactif!**
""")

st.balloons()

if st.button("Send balloons!"):
    st.balloons()


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
        title = img.get("alt").strip() if img else None

    
    
    for card, show in zip(cards, shows):

        

        img = card.find("img") 
        title = img.get("alt").strip() if img else None
        # url = card.get_attribute("href")
        href = card.get("href") 
        url = base_url + href if href and href.startswith("/") else href
        dates = show.find("p",class_="show_date")
        location = show.find("p",class_= "show_place")


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

'''st.subheader('Programmation Opera de Paris, saison 25/26')
st.write(f"Title : {e['title']}")
st.write(f"Dates : {e['dates']}")
                    
st.write(f"Total evenements ; {len(unique_events)}")'''

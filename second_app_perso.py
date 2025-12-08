from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from requests_html import HTMLSession
import random

print("trial")

def get_google_weather(city):

    url = f"https://www.google.com/search?q=meteo+{city}"

    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # vrai user-agent Chrome
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # Empêche Google de détecter Selenium
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        driver.get(url)

        # Pause randomisée pour imiter un humain
        time.sleep(random.uniform(1.5, 3.2))

        # Injection JS pour supprimer detection Selenium
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Attente des données météo
        temp_el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "wob_tm"))
        )

        temp = temp_el.text
        unit = driver.find_element(By.CSS_SELECTOR, "span.wob_t").text
        desc = driver.find_element(By.ID, "wob_dc").text
        humidity = driver.find_element(By.ID, "wob_hm").text
        wind = driver.find_element(By.ID, "wob_ws").text

        return {
            "city": city,
            "temp": f"{temp} {unit}",
            "description": desc,
            "humidity": humidity,
            "wind": wind
        }

    except Exception as e:
        print("Erreur :", e)
        return None

    finally:
        driver.quit()





"""base_url = "https://www.operadeparis.fr/programmation/saison-25-26"
page_segment = ["spectacles-opera", "ballet", "concert et récital", "jeune public"]   # ici tu peux changer selon la page
programming_url = f"{base_url}/{page_segment}"

print(programming_url)

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
    for segment in page_segment:
        programming_url = f"{base_url}/{segment}"
        driver.get(programming_url)


        WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "FeaturedList__card"))
        )

    soup = BeautifulSoup(driver.page_source, "html.parser")

    cards = soup.find_all("div", class_="FeaturedList__card")

    for card in cards:

        # Title = inside the img alt=""
        img = card.find("img")
        title = img["alt"].strip() if img else None

        # URL
        link = card.find("a", class_="FeaturedList__reserve-img")
        href = link["href"] if link else None
        url = base_url + href if href and href.startswith("/") else href

          # Dates
        date_tag1 = card.find("p", class_="FeaturedList__date")
        dates1 = date_tag1.get_text(strip=True) if date_tag1 else None

        # Location
        loc_tag1 = card.find("p", class_="FeaturedList__place")
        location1 = loc_tag1.get_text(strip=True) if loc_tag1 else None



        # Dates
        date_tag = card.find("p", p ="show_date")
        dates = date_tag.get_text(strip=True) if date_tag else None

        # Location
        loc_tag = card.find("p", p ="show_place")
        location = loc_tag.get_text(strip=True) if loc_tag else None

        events.append({
            "title": title,
            "dates": dates1,
            "location": location1,
            "url": url
        })


finally:
    driver.quit()

# Remove duplicates
unique = {e["url"]: e for e in events}.values()

# Print results
for e in unique:
    print(f"Titre  : {e['title']}")
    print(f"Dates  : {e['dates']}")
    print(f"Lieu   : {e['location']}")
    print(f"URL    : {e['url']}")
    print("-" * 40)

print(f"Total événements : {len(list(unique))}")

s = HTMLSession()


r = s.get("https://www.google.com")
print(r.status_code)


query = "paris"
url = f'https://www.google.com/search?q=google+weather+{query}'

r = s.get(url, headers = { "user agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" "AppleWebKit/537.36"})

temp = r.html.find('span#wob_tm', first=True)


#unit = r.html.find("div.vk_bk.wob-unit span.wob_t", first=True).text
#desc =  r.html.find("div.VQF4g", first=True).find("span#wob-dc", first=True)"""

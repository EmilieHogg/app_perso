#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import streamlit as st

# -----------------------------
# Fonction pour installer un module si nécessaire
# -----------------------------
def install_package(package_name):
    try:
        __import__(package_name)
    except ImportError:
        print(f"Module {package_name} manquant. Installation en cours...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

# Installer les packages nécessaires
for pkg in ["pandas", "streamlit", "numpy", "yfinance", "requests", "lxml", "beautifulsoup4"]:
    install_package(pkg)

# -----------------------------
# Imports principaux
# -----------------------------
import pandas as pd
import numpy as np
import yfinance as yf
import requests
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import urllib.parse
import datetime as dt

today = dt.datetime.today().strftime('%Y-%m-%d')
# -----------------------------
# URL Wikipédia CAC40
# -----------------------------
url = "https://fr.wikipedia.org/wiki/CAC_40"

# Crée la requête avec un User-Agent
req = Request(
    url,
    headers={
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/116.0.5845.96 Safari/537.36"
        )
    }
)

try:
    # Ouvre l'URL et lit le contenu HTML
    with urlopen(req) as response:
        html = response.read()

    # Utilise pandas pour lire les tables HTML
    tables = pd.read_html(html)
    print(f"{len(tables)} tables trouvées sur la page Wikipédia CAC 40.")

    

    # Vérifie toutes les tables pour trouver celle du CAC 40
    for i, table in enumerate(tables):
        if "Société" in table.columns or "Mnémo" in table.columns:
            cac40_table = table
            print(f"Table CAC40 trouvée à l'index {i} : {table.shape[0]} lignes, {table.shape[1]} colonnes")
            break
    else:
        raise ValueError("Impossible de trouver la table CAC40 sur la page.")

    # Affiche les 5 premières lignes
    print(cac40_table.head())

except HTTPError as e:
    print(f"Erreur HTTP: {e.code} {e.reason}")
except Exception as e:
    print(f"Erreur: {e}")

"""print(cac40_table.columns.tolist())
tickers = cac40_table.Mnémo.dropna().unique()
tickers = list(tickers)
print(tickers)
companies = cac40_table[['Société', 'Mnémo']].dropna()
print(companies)


today = dt.datetime.today().strftime('%Y-%m-%d')

tickers_yahoo = [ticker + ".PA" for ticker in tickers]
tickers_yahoo = ["MT.AS" if t == "MT.PA" else t for t in tickers_yahoo]
data =yf.download(tickers_yahoo, start = '2020-01-01', end =today)
closing_price = data['Close']
print(closing_price)'''

closing_price.to_csv('CAC40')"""



#st.set_page_config(page_title="CAC40 Dashboard", layout="wide")

#st.title("📈 CAC 40 Dashboard")

# Load CAC40 table

def load_cac40():
    url = "https://fr.wikipedia.org/wiki/CAC_40"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # raise error if blocked
    tables = pd.read_html(response.text)
    cac40_table = tables[2]
    return cac40_table[["Société", "Mnémo"]].dropna().drop_duplicates()

companies_df = load_cac40()

#st.subheader("CAC40 Companies")
#st.dataframe(companies_df)


# Build ticker list

tickers = companies_df["Mnémo"].tolist()
tickers_yahoo = [t + ".PA" for t in tickers]
tickers_yahoo = ["MT.AS" if t == "MT.PA" else t for t in tickers_yahoo]


# Download prices

@st.cache_data
def load_prices(tickers):
    today = dt.datetime.today().strftime('%Y-%m-%d')
    data = yf.download(tickers, start="2020-01-01", end=today)
    return data["Close"]

closing_price = load_prices(tickers_yahoo)

# Clean column names
closing_price.columns = [c.replace(".PA", "") for c in closing_price.columns]


# Mapping ticker -> Société
# -----------------------------
ticker_to_company = dict(companies_df.values)

closing_price_clean = closing_price.copy()
closing_price_clean.columns = [
    col.replace(".PA", "").strip()
    for col in closing_price_clean.columns
]
ticker_to_company = {
    k.strip(): v
    for k, v in companies_df[["Mnémo", "Société"]].values
}
# Rename columns from ticker to company name
closing_price_named = closing_price_clean.rename(columns=ticker_to_company)
print (closing_price_named.head())



closing_price_named.to_csv("CAC40_closing_prices_named.csv")

# Sidebar selector

selected_company = st.sidebar.selectbox(
    "Select a Company",
    companies_df["Société"]
)

selected_ticker = companies_df.loc[
    companies_df["Société"] == selected_company,
    "Mnémo"
].values[0]

# Show latest close

latest_price = closing_price[selected_ticker].iloc[-1]

#st.metric(
    #label=f"{selected_company} Latest Close",
    #value=f"{latest_price:.2f} €"
#)
# Price chart

#st.subheader(f"{selected_company} Price History")

#st.line_chart(closing_price[selected_ticker])
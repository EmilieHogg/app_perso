#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys

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
for pkg in ["pandas", "numpy", "yfinance", "requests", "lxml", "beautifulsoup4"]:
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
        if "Entreprise" in table.columns or "Nom" in table.columns:
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
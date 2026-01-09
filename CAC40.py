import pandas as pd
import numpy as np
import yfinance as yf
import requests
from urllib.request import Request, urlopen



#headers = {
#    "User-Agent": (
#       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
#       "AppleWebKit/537.36 (KHTML, like Gecko) "
#       "Chrome/131.0.0.0 Safari/537.36"
#   )
#}

#Use read_html with a headers parameter via requests

tables = pd.read_html("https://fr.wikipedia.org/wiki/CAC_40", 
    flavor="bs4"  # uses BeautifulSoup under the hood
)

# The first table on the page usually contains the CAC 40 components
cac40_table = tables[4]

print(cac40_table.head())  # print the first few rows
#req = Request("https://fr.wikipedia.org/wiki/CAC_40", headers=headers)
#html = urlopen(req).read().decode("utf-8")

#CAC40 = pd.read_html('https://fr.wikipedia.org/wiki/CAC_40')
#print(html[:500])

#print(CAC40)

import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
res = requests.get("http://www.bna.com.ar/")
soup = BeautifulSoup(res.content,'lxml')
table = soup.find_all('table', attrs={'class': 'table cotizacion'})[1]
df = pd.read_html(str(table), thousands=",", decimal=".")[0]
date = df.columns[0]
df.columns = ["MONEDA", (df.columns[1]).upper(), (df.columns[2]).upper()]
df['MONEDA'] = df['MONEDA'].map(lambda x: str.replace(x.upper(), '(*)', ''))
df.sort_values(by="MONEDA", inplace=True)
df.to_csv("bna_cotizaciones_por_fecha_"+str.replace(date, "/", "-")+".csv", index=False, quoting=csv.QUOTE_NONNUMERIC)
df

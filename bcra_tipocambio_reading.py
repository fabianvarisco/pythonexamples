import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
date = "11/07/2017" 
res = requests.get("http://www.bcra.gob.ar/PublicacionesEstadisticas/Cotizaciones_por_fecha_2.asp?date2=" + date)
soup = BeautifulSoup(res.content,'lxml')
table = soup.find_all('table')[0] 
df = pd.read_html(str(table), thousands=".", decimal=",", skiprows={0,1})[0].applymap(lambda x : "" if type(x) == str and len(x) == x.count("-") else x)
df.columns = df.columns.droplevel()
df.columns = ['MONEDA', 'DOLARES', 'PESOS_ARG']
df['MONEDA'] = df['MONEDA'].map(lambda x: x.upper())
df.sort_values(by="MONEDA", inplace=True)
df.to_csv("bcra_cotizaciones_por_fecha_"+str.replace(date, "/", "-")+".csv", index=False, quoting=csv.QUOTE_NONNUMERIC)
df

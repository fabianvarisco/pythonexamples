import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import datetime
import json

class QuoteSource:
    def __init__(self, date):
        assert isinstance(date, datetime.date), "QuoteSource.date must by Date"
        assert date < datetime.date.today(), "QuoteSource.date must by past"
        maxDays = 30
        assert date > datetime.date.today() - datetime.timedelta(maxDays), "QuoteSource.date must by past max [" + str(
            maxDays) + "] days"
        self.date = date

    def getSoupFromUrl(self, url):
        res = requests.get(url)
        return BeautifulSoup(res.content, 'lxml')

    def finalSets(self):
        if not self.isEmpty():
            self.df.replace(np.nan, '', regex=True, inplace=True)
            self.df.sort_values(by="currency", inplace=True)

    def isEmpty(self):
        return self.df.empty


class BNA(QuoteSource):
    def __init__(self, date):
        QuoteSource.__init__(self, date)

        self.url = "http://www.bna.com.ar/"
        soup = self.getSoupFromUrl(self.url)
        table = soup.find_all('table', attrs={'class': 'table cotizacion'})[1]
        self.df = pd.read_html(str(table), thousands=",", decimal=".")[0]
        resultDate = datetime.datetime.strptime(self.df.columns[0], "%d/%m/%Y").date()

        if self.date != resultDate:
            self.df = pd.DataFrame({'Empty': []})
            return

        assert self.df.columns[1] == "Compra", "BNA: Column 1 must be [Compra] but it's [" + self.df.columns[1] + "]"
        assert self.df.columns[2] == "Venta", "BNA: Column 2 must be [Compra] but it's [" + self.df.columns[2] + "]"

        self.df.columns = ["currency", "bna_bid_ARS", "bna_ask_ARS"]
        self.df['currency'] = self.df['currency'].str.upper()

        mask = self.df['currency'].map(lambda x: x.find('*') >= 0)
        self.df.loc[mask, 'bna_bid_ARS'] /= 100
        self.df.loc[mask, 'bna_ask_ARS'] /= 100

        self.df['currency'] = self.df['currency'].map(lambda x: str.replace(x, '(*)', '').strip())
        self.df['currency'] = self.df['currency'].map(lambda x: str.replace(x, 'U.S.A', 'ESTADOUNIDENSE'))
        self.df['currency'] = self.df['currency'].map(lambda x: str.replace(x, 'CORONAS', 'CORONA'))
        self.df['currency'] = self.df['currency'].map(lambda x: str.replace(x, 'DOLARES', 'DOLAR'))
        self.df['currency'] = self.df['currency'].map(lambda x: str.replace(x, 'YENES', 'YEN (JAPON)'))
        self.df['currency'] = self.df['currency'].map(lambda x: x[:-1] if x.endswith('S') else x)

        self.finalSets()


class BCRA(QuoteSource):
    def __init__(self, date):
        QuoteSource.__init__(self, date)

        self.url = "http://www.bcra.gob.ar/PublicacionesEstadisticas/Cotizaciones_por_fecha_2.asp?date2="
        soup = self.getSoupFromUrl(self.url + self.date.strftime("%d/%m/%Y"))
        table = soup.find_all('table')[0]
        self.df = pd.read_html(str(table), thousands=".", decimal=",", skiprows={0, 1})[0].applymap(
            lambda x: "" if type(x) == str and len(x) == x.count("-") else x)
        self.df.columns = ['currency', 'bcra_ask_USD', 'bcra_ask_ARS']
        self.df['currency'] = self.df['currency'].str.upper()

        self.finalSets()


def quoteCurrencyCollector(daysAgo=10):
    assert daysAgo > 0 and daysAgo <= 20, "quoteCurrencyCollector.daysAgo [" + str(
        daysAgo) + "] must be between 1 and 20"

    today = datetime.date.today()
    result_list = []

    for i in range(daysAgo, 0, -1):
        d = today - datetime.timedelta(i)
        sd = d.strftime("%Y-%m-%d")
        print("looking for [" + sd + "]...")

        bcra = BCRA(d)
        bna = BNA(d)

        print("len(result_list): " + str(len(result_list)))
        result_df = pd.DataFrame({'Empty': []})

        if not bcra.isEmpty() and not bna.isEmpty():
            print("BCRA and BNA found!!!")
            result_df = pd.merge(bcra.df, bna.df, how='outer')
        elif not bcra.isEmpty():
            print("BCRA found!!!")
            result_df = bcra.df
        elif not bna.isEmpty():
            print("BNA found!!!")
            result_df = bna.df

        if not result_df.empty:
            print("appending quotes to result_list...")
            result_dict = {"quote_date": sd, "quotes": result_df.to_dict(orient='records')}
            # print(result_dict)
            result_list.append(result_dict)
            print("len(result_list): " + str(len(result_list)))
            del result_dict

    print(result_list)
    return json.dumps(result_list)


print(quoteCurrencyCollector())

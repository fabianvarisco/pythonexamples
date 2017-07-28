import requests
import pandas as pd
import csv
import json
token="wsg0pK60DVpUUv5MFSamBy5Q0o5GWKwZYZ5t5XUuK4h2..."
#like this: token="wsg0pK60DVpUUv5MFSamBy5Q0o5GWKwZYZ5t5XUuK4h2..."

headers = {'authorization': "Bearer " + token, 'accept': "application/json" }
res = requests.get("https://api.commoprices.com/v1/imf", headers=headers)
res.status_code
j = res.json()["data"]
df=pd.DataFrame(j)
df.to_csv("api_commoprices_com_v1_imf.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)
df

dbname="PSMEA"
res = requests.get("https://api.commoprices.com/v1/imf/"+ dbname + "/data", headers=headers)
df=pd.DataFrame(res.json()["data"])
ds = df.loc["dataseries","request"]
df2 = pd.DataFrame(ds, columns=["DAY", "VALUE"])
df2.to_csv("api_commoprices_com_v1_imf_" + dbname + ".csv", index=False, quoting=csv.QUOTE_NONNUMERIC)
df2

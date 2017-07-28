import requests
import pandas as pd
token="wsg0pK60DVpUUv5MFSamBy5Q0o5GWKwZYZ5t5XUuK4h2fcrKTHAdEK7TeHjL"
#like this: token="wsg0pK60DVpUUv5MFSamBy5Q0o5GWKwZYZ5t5XUuK4h2..."

headers = {'authorization': "Bearer " + token, 'accept': "application/json" }
res = requests.get("https://api.commoprices.com/v1/imf", headers=headers)
res.status_code
j = res.json()["data"]
df=pd.DataFrame(j)
df

res = requests.get("https://api.commoprices.com/v1/imf/POILDUB/data", headers=headers)
res.status_code
j = res.json()["data"]
df=pd.DataFrame(j)
df

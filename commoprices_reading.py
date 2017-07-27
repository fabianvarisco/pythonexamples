import requests
token="wsg0pK60DVpUUv5MFSamBy5Q0o5GWKwZYZ5t5XUuK4h2fcrKTHAdEK7TeHjL"

headers = {'authorization': "Bearer " + token, 'accept': "application/json" }
res = requests.get("https://api.commoprices.com/v1/imf", headers=headers)
res.status_code
df=pd.DataFrame(res.json()["data"])
df


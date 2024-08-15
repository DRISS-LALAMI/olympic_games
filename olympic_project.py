import pandas as pd
#d = {'animals': ["elephant", "horse"], 'ranking': [1, 2]}
#df = pd.DataFrame(data=d)

#print(df.columns)
import requests

# The API endpoint URL
url = "https://bfortune.outscale-euw2.opendatasoft.com/api/explore/v2.1/catalog/datasets/summer/records?limit=100&refine=country%3A%22MAR%22"

# Make a GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()
    #print(data)
else:
    print(f"Request failed with status code {response.status_code}")

results = data["results"]

moroccan_athletes = pd.DataFrame(data=results)

moroccan_athletes.to_excel("moroccan-medals.xlsx")
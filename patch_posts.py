import os
import csv
import sys
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load Webflow API Key
load_dotenv()
api_key = os.getenv('API_KEY')

# Get collection id from args
if str(sys.argv[1]):
    collection_id = str(sys.argv[1])

print("Collection ID: " + collection_id)

# Get file path
if str(sys.argv[2]).endswith('.csv'):
    filepath = str(sys.argv[2])
else:
    print("Input valid filepath")

print("Posts will be updated from: " + filepath)

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer %s" %api_key
}

def patch_posts(col_id, item_id, payload, headers):
    url = "https://api.webflow.com/collections/%s/items/%s" %(col_id, item_id)

    response = requests.patch(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Updated %s (%s)" %(payload['slug'], item_id))
    
    else:
        print("Request Failed")
        print("Status code: %s" %response.status_code)

data = []

with open(filepath, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)
    print(data)

# ARCHIVE TRUE FOR TESTING
for item in data:
    payload = {"fields": {
            "slug": item['Slug'],
            "name": item['Updated Title'],
            "_archived": True,
            "_draft": False,
        }}
    patch_posts(
        collection_id,
        item['Id'],
        payload=payload,
        headers=headers
    )
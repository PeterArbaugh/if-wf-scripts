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

# Create csv filename
if (len(sys.argv) > 2 and sys.argv[2]):
    if str(sys.argv[2]).endswith('.csv'):
        filename = str(sys.argv[2])
    else:
        filename = str(sys.argv[2]) + '.csv'
else:
    timestamp = datetime.now()
    filename = "get_posts_%s.csv" %timestamp.strftime("%Y-%m-%d %H:%M:%S")

print("Posts will be saved as: " + filename)

def get_posts(id, fn):
    url = "https://api.webflow.com/collections/%s/items?limit=100" %id

    headers = {
        "accept": "application/json",
        "authorization": "Bearer %s" %api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # for item in data['items']:
        #     print([
        #         item['name']
        #     ])

        # Create csv
        with open(fn, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write header row
            writer.writerow(["Title", "Slug", "Id"])

            for item in data['items']:
                writer.writerow([
                    item['name'],
                    item['slug'],
                    item['_id']
                ])
    
    else:
        print("Request Failed")
        print("Status code: %s" %response.status_code)



get_posts(collection_id, filename)
import os
import csv
import sys
import requests
from lxml import etree
from dotenv import load_dotenv
from datetime import datetime

# Load Webflow API Key
load_dotenv()
api_key = os.getenv('API_KEY')

# Get collection id from args
if str(sys.argv[1]):
    collection_id = str(sys.argv[1])

print("Collection ID: " + collection_id)

# Check if content required
if (len(sys.argv) > 2 and sys.argv[2]):
    content = sys.argv[2]
    if content:
        print("Including post content in export...")

# Create csv filename
if (len(sys.argv) > 3 and sys.argv[3]):
    if str(sys.argv[2]).endswith('.csv'):
        filename = str(sys.argv[3])
    else:
        filename = str(sys.argv[3]) + '.csv'
else:
    timestamp = datetime.now()
    filename = "get_posts_%s.csv" %timestamp.strftime("%Y-%m-%d %H:%M:%S")

print("Posts will be saved as: " + filename)

# Clean content HTML
def remove_html_tags(text):
    if not text:  # Check if text is None or empty
        return ''
    
    try:
        parser = etree.HTMLParser()
        tree = etree.fromstring(text, parser)

        if tree is None:  # In case fromstring returns None
            return ''

        return etree.tostring(tree, encoding='unicode', method='text').strip()
    except (etree.XMLSyntaxError, TypeError, ValueError):
        # Handle any parsing issues or invalid HTML content
        return ''

# TO DO: Update for greater than 100 items
def get_posts(id, fn, content):
    url = "https://api.webflow.com/collections/%s/items?limit=100" %id

    headers = {
        "accept": "application/json",
        "authorization": "Bearer %s" %api_key
    }

    response = requests.get(url, headers=headers)

    print('Status code: ' + str(response.status_code))

    if response.status_code == 200:
        data = response.json()

        # Create csv
        if content == False:
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
        elif content:
            with open(fn, 'w', newline='') as file:
                writer = csv.writer(file)
                # Write header row
                writer.writerow(["Title", "Slug", "Id", "Post Type", "Client Name","Subtitle", "Post Content"])

                for item in data['items']:

                    post_content = (
                        item.get('post-content', '') +
                        item.get('content-block-2-what-we-did', '') +
                        item.get('content-block-3-impact', '')
                        )
                    
                    clean_content = remove_html_tags(post_content)

                    writer.writerow([
                        item.get('name', 'N/A'),  # Use .get() with a default value if the key doesn't exist
                        item.get('slug', 'N/A'),
                        item.get('_id', 'N/A'),
                        item.get('post-type', 'N/A'),
                        item.get('client-name', 'N/A'),
                        item.get('dek-subtitle', 'N/A'),
                        clean_content.strip()
                    ])
        else:
            print("Export failed.")
    
    else:
        print("Request Failed")
        print("Status code: %s" %response.status_code)



get_posts(collection_id, filename, content)
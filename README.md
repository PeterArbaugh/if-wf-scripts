# WebFlow Management Scripts for Intentional Futures

Python scripts to help manage our WebFlow marketing site.

## Usage
Accessing the API requires an API key for a specific site. These can be created under Sites -> Settings -> Integrations. The API key is saved in a `.env` file.

### Get Post Titles
Returns a list of post titles in csv format. Includes title, slug, and item id.

```python3 get_post_titles.py COLLECTION_ID [FILENAME]```

### Patch Posts
Patches each post item listed in a CSV. Currently set up for CSVs with a header row of:
```Title,Slug,Id,Updated Title```

Note that the file path to the csv is required.
```python3 get_post_titles.py COLLECTION_ID FILEPATH.csv```

## TO DO
- Update to handle more than 100 items (chunking)
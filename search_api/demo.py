import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.environ['API_KEY']
SEARCH_ENGINE_ID = os.environ['SEARCH_ENGINE_ID']
QUERY = os.environ['QUERY']
#print(API_KEY, SEARCH_ENGINE_ID, QUERY)

service = build("customsearch", "v1", developerKey=API_KEY)
res = service.cse().list(q=QUERY, cx=SEARCH_ENGINE_ID).execute()
for item in res['items']:
    print(item['title'] + "\n" + item['link'] + "\n")

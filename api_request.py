import requests
import json 
import os
import time
from hc_token import url, token


headers = {
    'Authorization': f'Bearer {token}'
}
cache_file = 'books_cache.json'

def fetch_books_from_api():
  all_data = {'data':{'books':[]}}
  limit = 1000
  offset = 0
  has_more_data = True
  retry_count = 0
  max_retries = 5
  total_books = 0

  with open(cache_file, 'w') as f:
    f.write('[')  # Start JSON array
    first_item = True

    while has_more_data:
      query = """
        {
          books(limit: %d, offset: %d) {
            rating
            title
            id
            user_books {
              rating
              user_id
            }
          }
        }
        """ % (limit, offset)

      response = requests.post(url, json={'query': query}, headers=headers)
      data = response.json()

      if 'error' in data and data['error'] == 'Throttled':
        if retry_count >= max_retries:
          print(f"Max retries reached at offset {offset}. Stopping.")
          break
      
        wait_time = 2 ** retry_count
        print(f"Throttled at offset {offset}. Waiting {wait_time} seconds...")
        time.sleep(wait_time)
        retry_count += 1
        continue
            
      retry_count = 0
      if 'errors' in data:
        print(f"Error at offset {offset}:", data['errors'])
        break

      if 'data' in data and 'books' in data['data']:
        new_items = data['data']['books']
        if not new_items:
          has_more_data = False
        else:
          for book in new_items:
            if not first_item:
                f.write(',\n')
            json.dump(book, f)
            first_item = False

          total_books += len(new_items)
          print(f"Offset {offset}: Fetched {len(new_items)} books. Total: {total_books}")
          offset += limit
          time.sleep(1)
      else:
        break

  return all_data

def get_books(refresh = False):
  if os.path.exists(cache_file) and not refresh:
    with open(cache_file, 'r') as f:
      return json.load(f)

  fetch_books_from_api()
  with open(cache_file, 'r') as f:
    return json.load(f)

full_data = get_books(refresh=True)
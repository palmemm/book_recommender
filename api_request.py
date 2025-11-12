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

  if os.path.exists(cache_file):
    print(f"Cache file already exists with data. Delete it first to re-fetch.")
    return total_books

  with open(cache_file, 'w') as f:

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

      try:
        response = requests.post(url, json={'query': query}, headers=headers)
        if not response.text or response.text.strip() == '':
          print(f"Empty response at offset {offset}. Retrying...")
          if retry_count >= max_retries:
            print(f"Max retries reached. Saved {total_books} books.")
            break
          retry_count += 1
          time.sleep(2 ** retry_count)
          continue
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
              if len(book['user_books']) > 1 and book['rating']:
                f.write(json.dumps(book) + '\n')
                total_books += 1

            print(f"Offset {offset}: Fetched {len(new_items)} books. Total: {total_books}")
            offset += limit
            time.sleep(1)
        else:
          print(f"Unexpected response structure at offset {offset}: {data}")
          break

      except requests.exceptions.JSONDecodeError as e:
        print(f"JSON decode error at offset {offset}:")
        print(f"Response status: {response.status_code}")
        print(f"Response text (first 500 chars): {response.text[:500]}")
        if retry_count >= max_retries:
            print(f"Max retries reached. Saved {total_books} books.")
            break
        retry_count += 1
        time.sleep(2 ** retry_count)
        continue

  return all_data

def get_all_books():
  if not os.path.exists(cache_file):
    fetch_books_from_api()
  
  books = []
  with open(cache_file, 'r') as f:
    for line in f:
      books.append(json.loads(line))

  return books

def get_one_book():
  #loads books one at a time
  if not os.path.exists(cache_file):
    fetch_books_from_api()
    
  with open(cache_file, 'r') as f:
    for line in f:
      yield json.loads(line)



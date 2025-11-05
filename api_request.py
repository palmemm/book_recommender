from hc_token import url, token
import requests

headers = {
    'Authorization': f'Bearer {token}'
}

query = """
{
  books {
    rating
    title
    id
    cached_tags
    user_books {
      rating
      id
      user_id
      book_id
    }
  }
}
"""

response = requests.post(url, json={'query': query}, headers=headers)
data = response.json()

#This spits a dictionary of length 1 with the key 'data'

full_data = data['data']



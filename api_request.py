from token import url, token
import requests

headers = {
    'Authorization': f'Bearer {token}'
}

query = """
{
  user_books {
    book_id
    id
    rating
    read_count
  }
}
"""

response = requests.post(url, json={'query': query}, headers=headers)
data = response.json()
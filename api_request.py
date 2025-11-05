import requests

url = 'https://api.hardcover.app/v1/graphql'

token = 'eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJIYXJkY292ZXIiLCJ2ZXJzaW9uIjoiOCIsImp0aSI6IjA2OWM2ZGU0LTk1NmQtNDhkMC1iYTBjLTFlMzczNmFjZTk3ZSIsImFwcGxpY2F0aW9uSWQiOjIsInN1YiI6IjUzMzIyIiwiYXVkIjoiMSIsImlkIjoiNTMzMjIiLCJsb2dnZWRJbiI6dHJ1ZSwiaWF0IjoxNzYyMzEyNDE0LCJleHAiOjE3OTM4NDg0MTQsImh0dHBzOi8vaGFzdXJhLmlvL2p3dC9jbGFpbXMiOnsieC1oYXN1cmEtYWxsb3dlZC1yb2xlcyI6WyJ1c2VyIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6InVzZXIiLCJ4LWhhc3VyYS1yb2xlIjoidXNlciIsIlgtaGFzdXJhLXVzZXItaWQiOiI1MzMyMiJ9LCJ1c2VyIjp7ImlkIjo1MzMyMn19.fvQ1Mt32O1AY52jnrplw0W4WWiRK-b9F75Tu-zAoT6I'

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
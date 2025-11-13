import pandas as pd
import json
from api_request import get_one_book

user_ratings = {}
book_title_cache = 'book_title_cache.json'

with open(book_title_cache, 'w') as f:

    for book in get_one_book():
        book_id = book['id']
        f.write(json.dumps({book_id:book['title']}) + '\n')
        user_ratings['Average'] = {book_id:book['rating']}
        for user in book['user_books']:
            user_id = user['user_id']
            if user_id in user_ratings.keys():
                user_ratings[user_id][book_id] = user['rating']
            else:
                user_ratings[user_id] = {book_id:user['rating']}

rating_df = pd.DataFrame(user_ratings)
print(rating_df.info())

#Want to create a user-item matrix so will take the transpose. Then will delete all rows with only null values
rating_df = rating_df.T

rating_df = rating_df.dropna(axis=0, how='all') 
rating_df = rating_df.dropna(axis=1, how='all')
print(rating_df.info())

import pandas as pd
from api_request import get_one_book

user_ratings = {}
book_titles = {}

for book in get_one_book():
    avg_rating = book['rating']
    book_id = book['id']
    book_title = book['title']
    book_titles[book_id] = book_title
    user_ratings['Average'] = {book_id:avg_rating}
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

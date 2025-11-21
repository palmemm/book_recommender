import pandas as pd
import json
from scipy.sparse import lil_matrix
import numpy as np
from api_request import get_one_book

user_to_idx = {'Average':0}
book_to_idx = {}
# book_title_cache = 'book_title_cache.json'
book_titles = {}

# with open(book_title_cache, 'w') as f:

for book in get_one_book():
    book_id = book['id']
    if book_id not in book_to_idx:
        book_to_idx[book_id] = len(book_to_idx)
    book_titles[book_id] = book['title']
    # f.write(json.dumps({book_id:book['title']}) + '\n')
    
    for user in book['user_books']:
        user_id = user['user_id']
        if user_id not in user_to_idx:
            user_to_idx[user_id] = len(user_to_idx)

n_books = len(book_to_idx)
n_users = len(user_to_idx)
ratings_matrix = lil_matrix((n_books, n_users), dtype=np.float32)

for book in get_one_book():
    book_idx = book_to_idx[book['id']]
    ratings_matrix[book_idx, 0] = book['rating']
    for user in book['user_books']:
        user_idx = user_to_idx[user['user_id']]
        ratings_matrix[book_idx, user_idx] = user['rating']
        
rating_df = pd.DataFrame.sparse.from_spmatrix(ratings_matrix, columns=user_to_idx.keys(), index=book_to_idx.keys())
print(rating_df.info())

#Want to create a user-item matrix so will take the transpose. First will delete all users with only null/0 values
col_sums = rating_df.sum(axis=0)
rating_df = rating_df.loc[:, col_sums>0]
rating_df = rating_df.T

print(rating_df.info())
print(rating_df.head(10))
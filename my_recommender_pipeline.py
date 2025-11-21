import json
from data_cleanup import rating_df, book_titles

# This file will recommend books to me based on my top-rated books, and will show me books 
# that other users who rated those books highly rated highly.

# Step 1: Extract my user id
# Since this is just for funsies, will have it pull my user id and will recommend books to myself. 
# In theory, this could be applied to any user in the df

my_id = 53322

#Step 2: Extract books I rated 4 stars or higher and pull the titles to see which books made the cut
my_ratings = rating_df.loc[my_id]

liked_books = []
for book_id,rating in my_ratings.items():
    if rating >= 4:
        liked_books.append(book_id)

# book_titles = []
# with open('book_title_cache.json', 'r') as f:
#     for line in f:
#         book_titles = json.loads(line)


liked_book_titles = [book_titles[book_id] for book_id in liked_books]

print(len(liked_book_titles))
print(liked_book_titles)

#Step 3: Find other users who rated those books highly

from data_cleanup import rating_df, book_titles

# This file will recommend books to a user based on their top-rated books, and will show them books 
# that other users who rated those books highly rated highly.

# Step 1: Pick a random user
# Since this is just for funsies, will have it pull my user id and will recommend books to myself. 
# In theory, this could be applied to any user in the df

my_id = 53322

my_ratings = rating_df.loc[my_id]

liked_books = []
for book_id,rating in my_ratings.items():
    if rating >= 4:
        liked_books.append(book_id)

liked_book_titles = [book_titles[book_id] for book_id in liked_books]
print(len(liked_book_titles))
print(liked_book_titles)

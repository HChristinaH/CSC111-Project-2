from my_librarian_manager_data import *

genres = get_genres("data/goodreads_book_genres_initial.json")
genres_list = genres[0]
authors = load_authors("data/goodreads_book_authors.json")
books_to_display = list(load_books(genres[1], authors, "data/goodreads_books_medium.json"))

books = list(books_to_display)
tree = load_tree(genres_list, books)

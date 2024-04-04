"""This file loads all the data from my_library_manager_data.py. Exported to the other files 
Copyright 2024 Areesha Abidi
"""
from my_library_manager_data import *

genres = get_genres("data/goodreads_book_genres_initial.json")
genres_list = genres[0]
authors = load_authors("data/goodreads_book_authors.json")
books_to_display = list(load_books(genres[1], authors, "data/goodreads_books_medium.json"))

books = list(books_to_display)
tree = load_tree(genres_list, books)

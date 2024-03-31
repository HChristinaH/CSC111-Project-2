"""This program contains classes for book and tree data structures used in the My AI Librarian program.
It also contains methods for loading these data structures from data files."""
from __future__ import annotations
from typing import Optional, Any
import json


class Book:
    """A Book object that represents a book's data from GoodReads.
    """
    # Instance Attributes:
    #     - isbn: unique ID of a book
    #     - title: title of the book
    #     - authors: list of authors
    #         [''] if no information is available
    #     - genre_shelves: a dictionary mapping each genre to its frequency of being shelved
    #     - all_shelves: a dictionary mapping each shelf to its frequency
    #     - average_rating: the average rating of a book from 1.0 to 5.0
    #         -1 if there is no information
    #     - ratings_count: the number of ratings
    #         -1 if there is no information
    #     - length: the length of a book
    #         1 is short, 0 - 200 pages(inclusive)
    #         2 is medium, 201 - 500 pages(inclusive)
    #         3 is long, 501 + pages.
    #         -1 if no information on number of pages
    #     - description: description of a book
    #     - pub_year: publication year of a book
    #     - book_url: link to book on GoodReads
    #     - image_url: link to JPEG image of book cover

    isbn: str
    title: str
    authors: list[str]
    genres: set[str]
    average_rating: float
    ratings_count: int
    length: int
    description: str
    pub_year: str
    book_url: str
    image_url: str

    def __init__(self, isbn: str, title: str, authors: list[str], genres: set[str], average_rating: float,
                 ratings_count: int, length: int, description: str, pub_year: str, book_url: str,
                 image_url: str) -> None:
        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.genres = genres
        self.average_rating = average_rating
        self.ratings_count = ratings_count
        self.length = length
        self.description = description
        self.pub_year = pub_year
        self.book_url = book_url
        self.image_url = image_url

    def __str__(self) -> str:
        """Represent a book as its title.
        """
        return self.title

    def similar_books(self, library: set[Book]) -> list[Book]:
        """Return a list of books in library ordered by decreasing similarity to self

        Preconditions:
            - self not in library"""
        scores = []  # maps a book to its similarity score with self
        for book in library:
            scores.append([book, self.similarity_score(book)])
        scores.sort(key=lambda x: x[1], reverse=True)

        return [row[0] for row in scores]

    def similarity_score(self, other: Book) -> float:
        """Calculate the similarity score between self and other book based on its genres.
        Similarity formula is calculated by common genres divided by total genres.
        """

        if len(self.genres) == 0 or len(other.genres) == 0:
            return 0
        else:
            return len(set.intersection(self.genres, other.genres)) / len(set.union(self.genres, other.genres))

    def average_similarity_score(self, library: Library) -> float:
        """Return the average similarity score of a book to all the books in the library
        Return 0.0 if there are no books in the library.
        """
        total_score = 0.0
        total_count = 0

        for saved_book in library.saved_books:
            total_score += self.similarity_score(saved_book)
            total_count += 1

        if total_count != 0:
            return total_score / total_count
        else:
            return 0.0

    def get_sequence(self, genre_list: list[str]) -> list[int | Book]:
        """Return the sequence of a book with respect to the list of genres"""

        sequence = [int(self.average_rating), self.length]

        for genre in genre_list:
            if genre in self.genres:
                sequence.append(1)
            else:
                sequence.append(0)

        # Add book to the end of the sequence
        sequence.append(self)

        return sequence


class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.

    Representation Invariants:
        - self._root is not None or self._subtrees == []
        - all(not subtree.is_empty() for subtree in self._subtrees)
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item.
    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return self._str_indented(0).rstrip()

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            str_so_far = '  ' * depth + f'{self._root}\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                str_so_far += subtree._str_indented(depth + 1)
            return str_so_far

    def is_empty(self) -> bool:
        """Return whether this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def insert_sequence(self, sequence: list[int | Book]) -> None:
        """Insert a book into the tree given its corresponding sequence.
        A book can be represented as a seqeuence in the format
         [<rating>, <length>, 0, 1, 0, 0, 1, ..., book object]."""

        # Base case - If the sequence is an empty list, there is nothing left to insert
        if not sequence:
            return
        # Recursive case
        else:
            # Check if first item of the sequence exists in a subtree
            tree = None
            for t in self._subtrees:
                if sequence[0] == t._root:
                    tree = t
                    break
            # If the first item of the list already exists as a subtree, insert sequence[1:] into it
            if tree is not None:
                tree.insert_sequence(sequence[1:])

            # Otherwise, create a new subtree with the first item as the item, and insert sequence[1:] into it
            else:
                tree = Tree(sequence[0], [])
                self._subtrees.append(tree)
                tree.insert_sequence(sequence[1:])

    def get_books(self, sequence: list[int]) -> set[Book]:
        """Return the set of all the books that correspond to the given sequence

        >>> book_tree = Tree(0, [])
        >>> book_tree.insert_sequence([3, 2, 1])
        >>> book_tree.get_books([3, 2]) == {1}
        True
        >>> book_tree.get_books([3, 2, 1])
        set()
        """
        books = set()
        if not sequence:
            if not self._subtrees:
                return books
            else:
                return {tree._root for tree in self._subtrees}
        else:
            for t in self._subtrees:
                if sequence[0] == t._root:
                    return t.get_books(sequence[1:])

            return books

    def get_books_differ_by(self, sequence: list[int], n: int) -> Optional[set[Book]]:
        """Return a set of all books with a sequence that differs from the given sequence by at most n levels.

        Preconditions:
            - n >= 0
        """

        if not sequence:
            if not self._subtrees:
                return set()
            else:
                return {tree._root for tree in self._subtrees}
        elif n == 0:
            return self.get_books(sequence)
        else:
            books = set()
            for t in self._subtrees:
                if t._root == sequence[0]:
                    books = books.union(t.get_books_differ_by(sequence[1:], n))
                else:
                    books = books.union(t.get_books_differ_by(sequence[1:], n - 1))

        return books

    def get_books_filter(self, filter_sequence: list[int], sort_by: str, library: Library,
                         height: int = 0) -> list[Book]:
        """Get all books that satisfy the given sequence sorted by the given category.
        The filter sequence is a binary sequence in the format [<rating 1>, <rating 2>, ... <rating 5>,
        <length 0>, ... length<2>, <genre 0>, <genre 1> ...]
        Note that genre number corresponds to its index in the genre list.
        If any of these categories is selected, they will have a value of 1 and 0 otherwise.
        The returned set of books will return all books that have the selected categories.
        If more than one rating or length filter is selected, each book will have one of the selected ratings
        or lengths.
        Each book will have all the selected genres.

        If sort_by == "Similarity", the books are sorted by average similarity to all book in the library.

        The height variable keeps track of the height of the tree being recursed on. It is only needed to
        differentiate rating, length, and genre categories.

        Preconditions:
            - sort_by in {"Similarity", "Popularity", "Average rating (high to low)",
            "Author (A-Z)", "Publication year"}
        """
        if height == 0:
            # Check indices 0 - 4 for rating
            return self.get_books_filter_helper(filter_sequence, sort_by, library, height, 5)

        elif height == 1:
            # Check indices 5 - 7 for length filter
            return self.get_books_filter_helper(filter_sequence, sort_by, library, height, 3)

        # Check indices 8+ for genre filters
        else:

            if not filter_sequence:
                if not self._subtrees:
                    return []
                else:
                    books = {tree._root for tree in self._subtrees}
                    return sort_books_by(books, sort_by, library)

            books = []
            if filter_sequence[0] == 0:
                for t in self._subtrees:
                    books += t.get_books_filter(filter_sequence[1:], sort_by, library, height + 1)
            else:
                sublists = [subtree.get_books_filter(filter_sequence[1:], sort_by, library, height + 1) for subtree in
                            self._subtrees if subtree._root == 1]
                for lst in sublists:
                    books += lst

            return books

    def get_books_filter_helper(self, filter_sequence: list[int], sort_by: str, library: Library,
                                height: int, n: int) -> list[Book]:
        """Handles the base case of rating and length filters, where n is the number of options in each category.
        For example, n = 5 if filter_sequence is on rating, and n = 3 if it is on length.
        Note that there is an off-by-one error since the indices of filter sequence begin from 0
        while the ratings and lengths begin from 1.
        Preconditions:
            - The first n elements of filter_sequence correspond to the filters of the category
        """
        filters = set()
        books = []
        for i in range(1, n + 1):
            if filter_sequence[i - 1] == 1:
                filters.add(i)

        if not filters:
            for t in self._subtrees:
                books += t.get_books_filter(filter_sequence[n:], sort_by, library, height + 1)
            return books
        else:
            for t in self._subtrees:
                if t._root in filters:
                    books += t.get_books_filter(filter_sequence[n:], sort_by, library, height + 1)
            return books


def get_genres(genre_file: str) -> tuple[list[str], dict[str, set[str]]]:
    """Create a list of genres and a dictionary mapping each book id to set of its genres.

    We will have a sequence like [<rating>, <length>, 0, 1, 0, 0, 1, ...]
    where each index beginning from 2 corresponds to a genre.
    For example, in this sequence, the genre corresponding to indices 1 and 4 are selected.
    """
    genre_list = []
    book_genres = {}  # maps book_id to genres
    index = 2

    with open(genre_file, 'r') as file:
        for line in file:
            entry = json.loads(line)
            book_id = entry["book_id"]
            genres = set(entry["genres"])  # gets genres only, ignores the frequency

            # Update book_id and genre mapping
            book_genres[book_id] = genres

            # Update genre list
            for genre in genres:

                if genre not in genre_list:
                    genre_list.append(genre)
                    index += 1

    return genre_list, book_genres


class Library:
    """A libary that contains a collection of books saved by the user
    """
    # Instance Attributes:
    #   - saved_books: set of all books in the library

    saved_books: set[Book]

    def __init__(self) -> None:
        """Initialize a library object
        """
        self.saved_books = set()

    def add(self, book: Book) -> None:
        """Save a new book
        """
        self.saved_books.add(book)

    def remove(self, book: Book) -> None:
        """Remove a book from the library.
        Raise ValueError if the book is not in the library
        """
        if book in self.saved_books:
            self.saved_books.remove(book)
        else:
            raise ValueError


def load_authors(authors_file: str) -> dict[str, str]:
    """Return a mapping of author_id to author name.
    """
    authors = {}
    with open(authors_file, 'r') as file:
        for line in file:
            entry = json.loads(line)
            authors[entry["author_id"]] = entry["name"]
    return authors


def load_books(book_genres: dict[str, set[str]], authors_mapping: dict[str, str], book_file: str) -> set[Book]:
    """Return a set of book objects with the information cross-referenced from the mappings and data file.
    book_genres maps a book_id to a set of its genres, and authors maps an author_id to an author's name.

    Preconditions:
        - each book_id in the book file is a key in book_genres
    """
    books = set()
    with open(book_file, 'r') as file:
        for line in file:
            entry = json.loads(line)
            book_id = entry["book_id"]
            isbn = entry["isbn"]
            title = entry["title"]
            authors = get_authors(entry["authors"], authors_mapping)
            genres = book_genres[book_id]
            average_rating = get_average_rating(entry["average_rating"])
            ratings_count = get_ratings_count(entry["ratings_count"])
            length = get_length(entry["num_pages"])
            description = entry["description"]
            pub_year = entry["publication_year"]
            book_url = entry["url"]
            image_url = entry["image_url"]
            book = Book(isbn, title, authors, genres, average_rating, ratings_count, length, description, pub_year,
                        book_url, image_url)
            books.add(book)

    return books


def get_length(num_pages: str) -> 0:
    """Get the length of a book.
    0-200 (inclusive) returns length 0.
    201-500 (inclusive) returns length 1.
    501 + returns length 2
    Return -1 if the number of pages is empty.
    """
    if num_pages == '':
        return -1

    num_pages = int(num_pages)

    if num_pages <= 200:
        return 1
    elif num_pages <= 500:
        return 2
    else:
        return 3


def get_average_rating(data: str) -> float:
    """Return the average rating of a book from the given data.
    Data is the average_rating of the book in string format.
    """
    if data == '':
        return -1.0
    else:
        return float(data)


def get_ratings_count(data: str) -> int:
    """Return the ratings count of a book from the given data.
    Data is the ratings_count of the book in string format.
    """
    if data == '':
        return -1
    else:
        return int(data)


def sort_books_by(books: set[Book], sort_by: str, library: Optional[Library] = None) -> list[Book]:
    """Sorts a set of books by the given category.
    Preconditions:
        - sort_by != "Similarity" or library is not None
        - sort_by in {"Similarity", "Popularity", "Average rating (high to low)", "Author (A-Z)",
                        "Publication year"}
    """
    if sort_by == "Similarity":
        return sort_by_similarity(books, library)

    book_list = list(books)
    if sort_by == "Popularity":
        book_list.sort(key=lambda book: book.ratings_count, reverse=True)

    elif sort_by == "Average rating (high to low)":
        book_list.sort(key=lambda book: book.average_rating, reverse=True)

    elif sort_by == "Author (A-Z)":
        book_list.sort(key=lambda book: book.authors[0])

    else:
        book_list.sort(key=lambda book: book.pub_year, reverse=True)

    return book_list


def sort_by_similarity(books: set[Book], library: Library) -> list[Book]:
    """Sort books by descending average similarity to books in the library
    """
    similarity_score_map = []  # each element is a list containing book and its average similarity score to library
    for book in books:
        similarity_score_map.append([book, book.average_similarity_score(library)])

    similarity_score_map.sort(key=lambda x: x[1], reverse=True)

    return [row[0] for row in similarity_score_map]


def get_authors(data: list[dict[str, str]], authors: dict[str, str]) -> list[str]:
    """Return a list of authors from the list of authors from a data entry
    An example of data is [{"author_id": "2983296", "role": ""}, {"author_id": "40075", "role": "Foreword by"}]
    If no authors are listed, return [''].
    """
    result = []
    for author in data:
        assert isinstance(author, dict)
        result.append(authors[author["author_id"]])
    if not result:
        result.append('')
    return result


def load_tree(genre_list: list[str], books: set[Book]) -> Tree:
    """Create a tree from the list of genres and set of books.
    The tree stores information as follows:
        - Root is 0 (this would be Level 0)
        - Each level of the tree corresponds to a specific attribute
        - Level 1 describes the rating of the book. If s is the subtree that
         contains level 1, then s[0] would be a rating of 1, s[1] would be
         a rating of 2 and so on.
        - Level 2 describes the length of the book. If s is the subtree that
        contains level 2, then s[0] would be short, s[1] would be medium, and s[2]
        would be long.
        - Level n where n is greater than or equal to 3 and corresponds to whether or not
        the book has been shelved under the genre or not, where n corresponds to the genre_list's element
        at index n - 3
    >>> genre_list, book_genres = get_genres("goodreads_book_genres_initial.json")
    >>> authors_mapping = load_authors("goodreads_book_authors.json")
    >>> books = load_books(book_genres, authors_mapping, "goodreads_books_small.json")
    >>> tree = load_tree(genre_list, books)
    """

    book_tree = Tree(0, [])
    for book in books:
        sequence = book.get_sequence(genre_list)
        book_tree.insert_sequence(sequence)

    return book_tree

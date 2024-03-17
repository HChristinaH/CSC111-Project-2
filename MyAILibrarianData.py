"""project description"""
from __future__ import annotations
from typing import Optional, Any

# TODO: check code with PythonTA once this is done

class Book:
    """A Book object that represents a book's data from GoodReads.
    Representation Invariants:
        - all isbns must be different # TODO: turn this into actual code
    """
    # Instance Attributes:
    #     - isbn: unique ID of a book
    #     - title: title of the book
    #     - genre_shelves: a dictionary mapping each genre to its frequency of being shelved
    #     - all_shelves: a dictionary mapping each shelf to its frequency
    #     - average_rating: the average rating of a book from 1 to 5
    #     - length: the length of a book
    #         Short length is 0 - 200 pages(inclusive)
    #         Medium is 201 - 500 pages(inclusive)
    #         Long is 501 + pages.
    #     - description: description of a book
    #     - pub_year: publication year of a book
    #     - book_url: link to book on GoodReads
    #     - image_url: link to JPEG image of book cover

    # TODO: create instance attributes with their type annotations

    def similar_books(self, library: set[Book]) -> list[Book]:
        """Return a list of books in library ordered by decreasing similarity to self"""

        # TODO: implement this method

    def similarity_score(self, other: Book) -> float:
        """Calculate the similarity score between self and other book.
        # TODO: create a formula for similarity score
        """

        # TODO: implement this method


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

    def insert_sequence(self, seqeunce: list[int]) -> None:
        """Insert a book into the tree given its corresponding sequence.
        A book can be represented as a seqeuence in the format
         [<rating>, <length>, 0, 1, 0, 0, 1, ...]."""
        # TODO: implement this method


def get_genres(genre_file: str) -> dict[str, int]:
    """Create a dictionary mapping each genre to an index starting from 2

    We will have a sequence like [<rating>, <length>, 0, 1, 0, 0, 1, ...]
    where each index beginning from 2 corresponds to a genre.
    For example, in this sequence, the genre corresponding to indices 3 and 6 are selected.
    """

    # TODO: implement this function


def load_tree(genre_file: str, full_file: str) -> Tree:
    """Create a tree from the given book data files.
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
        the book has been shelved under the genre mapping to index n - 1"""

    # TODO: implement this function using insert sequence

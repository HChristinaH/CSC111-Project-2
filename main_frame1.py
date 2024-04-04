"""This file creates all the elements that are on the top of the window. Major elements include the search bar and the saved books button

Copyright 2024 Areesha Abidi
"""
import tkinter as tk
from ttkbootstrap import ttk
from bookpage import saved_books_library
from scroll_frame import ScrollingFrame
from gettingdata import books_to_display as all_books


def saved_books_window() -> None:
    """ This function opens the (toplevel) window for the Saved books page.
    Works as the command for the saved button"""
    # Create a new instance of Toplevel
    saved_books_top = tk.Toplevel()

    saved_books_title = ttk.Label(saved_books_top, text="Your Saved Books", font="Arial, 15")
    saved_books_title.grid(row=0, column=0, pady=10)

    # Create a ScrollingFrame instance passing the saved_books_top Toplevel and saved books (Books)
    saved_books_scrolling_frame = ScrollingFrame(saved_books_top, saved_books_library.library)
    saved_books_scrolling_frame.grid(row=1, column=0)


def search_books(search_entry) -> None:
    """ Opens the search results for the input user makes in Entry 'search_entry'"""
    search_text = search_entry.get()  # Get the input
    if search_text:
        # Get all the Books that have the search_text str in their title
        filtered_books = [book for book in all_books if search_text.lower() in book.title.lower()]
        if filtered_books:
            search_top = tk.Toplevel()  # Create a new instance of Toplevel
            title_label = ttk.Label(search_top, text=f"Books containing '{search_text}' in title", font="Arial, 15")
            title_label.grid(row=0, column=0, pady=10)
            scrolling_frame = ScrollingFrame(search_top, filtered_books)
            scrolling_frame.grid(row=1, column=0)


class Frame1Main(ttk.Frame):
    """Displays the top frame of the main window. Includes access to search, and saved books"""
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self) -> None:
        """ Create widgets inside the top frame"""
        page_title = ttk.Label(self, text="My Library Manager", font='Arial, 15', padding=18)
        page_title.grid(row=0, column=1, sticky="nesw")

        spacer = ttk.Label(self, width=20)
        spacer.grid(row=0, column=2, sticky="nesw")

        search_entry = ttk.Entry(self, width=40)
        search_entry.grid(row=0, column=4, sticky="ew", padx=5)

        search_button = ttk.Button(self, text="Search", command=lambda: search_books(search_entry))
        search_button.grid(row=0, column=5, sticky="w", padx=5)

        spacer = ttk.Label(self, width=30)
        spacer.grid(row=0, column=6, sticky="nesw")

        saved_books_button = ttk.Button(self, text="Saved Books", command=saved_books_window)
        saved_books_button.grid(row=0, column=7, sticky="nesw", padx=5)

        # Line under the frame for design
        visible_spacer = ttk.Label(self, width=4, font='Arial, 2', background="black")
        visible_spacer.grid(row=1, column=0, columnspan=15, sticky="ew")

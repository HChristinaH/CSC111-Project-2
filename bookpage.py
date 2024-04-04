import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import requests
from io import BytesIO
import webbrowser
from PIL.ImageTk import PhotoImage
from my_librarian_manager_data import sort_books_by
from gettingdata import books


class SavedBooks:
    """Class that will keep the books in saved. Instances will be called on and mutated from different files"""
    # Instance Attributes:
    #     - library: set of saved by user books
    library: list

    def __init__(self) -> None:
        self.library = []

    def add_book(self, book):
        if book not in self.library:
            self.library.append(book)

    def remove_book(self, book):
        self.library.remove(book)


# Create the (one and only) instance of SavedBooks to store the saved books
saved_books_library = SavedBooks()


def create_book_page(book) -> None:
    root = tk.Toplevel()
    root.title("Book Information Page")

    root.resizable(False, False)  # Make the window unresizable

    # Load cover image from URL
    cover_image = load_cover_image(root, book.image_url, 200, 273)
    cover_label = ttk.Label(root, image=cover_image)
    cover_label.grid(row=0, column=0, rowspan=10, padx=10, pady=10, sticky="nw")

    # Display book information
    ttk.Label(root, text="Title:").grid(row=0, column=1, sticky="w", padx=10, pady=5)
    title_label = ttk.Label(root, text=book.title, wraplength=300)
    title_label.grid(row=0, column=2, sticky="w", padx=10, pady=5)

    ttk.Label(root, text="Authors:").grid(row=1, column=1, sticky="w", padx=10, pady=5)
    authors_label = ttk.Label(root, text=", ".join(book.authors), wraplength=300)
    authors_label.grid(row=1, column=2, sticky="w", padx=10, pady=5)

    ttk.Label(root, text="Genres:").grid(row=2, column=1, sticky="w", padx=10, pady=5)
    genres_label = ttk.Label(root, text=", ".join(book.genres), wraplength=300)
    genres_label.grid(row=2, column=2, sticky="w", padx=10, pady=5)

    ttk.Label(root, text="ISBN:").grid(row=3, column=1, sticky="w", padx=10, pady=5)
    isbn_label = ttk.Label(root, text=book.isbn, wraplength=300)
    isbn_label.grid(row=3, column=2, sticky="w", padx=10, pady=5)

    ttk.Label(root, text="Average Rating:").grid(row=4, column=1, sticky="w", padx=10, pady=5)
    avg_rating_label = ttk.Label(root, text=book.average_rating, wraplength=300)
    avg_rating_label.grid(row=4, column=2, sticky="w", padx=10, pady=5)

    ttk.Label(root, text="Ratings Count:").grid(row=5, column=1, sticky="w", padx=10, pady=5)
    ratings_count_label = ttk.Label(root, text=book.ratings_count, wraplength=300)
    ratings_count_label.grid(row=5, column=2, sticky="w", padx=10, pady=5)

    ttk.Label(root, text="Description:").grid(row=7, column=1, sticky="w", padx=10, pady=5)
    description_text = tk.Text(root, width=40, height=10, wrap="word")
    description_text.insert(tk.END, book.description)
    description_text.configure(state='disabled')
    description_text.grid(row=7, column=2, padx=10, pady=5, sticky="w")

    ttk.Label(root, text="Publication Year:").grid(row=8, column=1, sticky="w", padx=10, pady=5)
    pub_year_label = ttk.Label(root, text=book.pub_year, wraplength=300)
    pub_year_label.grid(row=8, column=2, sticky="w", padx=10, pady=5)

    ttk.Label(root, text="Goodreads:").grid(row=9, column=1, sticky="w", padx=10, pady=5)
    url_label = ttk.Label(root, text=book.book_url, wraplength=300, cursor="hand2", foreground="blue")
    url_label.grid(row=9, column=2, sticky="w", padx=10, pady=5)
    url_label.bind("<Button-1>", lambda e: webbrowser.open_new(book.book_url))

    # Buttons for adding and removing from saved
    if book not in saved_books_library.library:
        add_to_saved_button = ttk.Button(root, text="Add to Saved",
                                         command=lambda: add_to_saved(book, add_to_saved_button))
        add_to_saved_button.grid(row=10, column=1, padx=10, pady=5)
    else:
        add_to_saved_button = ttk.Button(root, text="Added!", style="Red.TButton", state="disabled")
        add_to_saved_button.grid(row=10, column=1, padx=10, pady=5)

    remove_from_saved_button = ttk.Button(root, text="Remove from Saved",
                                          command=lambda: remove_from_saved(book, add_to_saved_button,
                                                                            remove_from_saved_button))
    if book in saved_books_library.library:
        remove_from_saved_button.grid(row=10, column=2, padx=10, pady=5)

    # Create frame for Similar Books section
    similar_books_frame = ttk.Frame(root)
    similar_books_frame.grid(row=12, column=0, columnspan=3, pady=10, sticky="s")

    # Label for Similar Books
    ttk.Label(similar_books_frame, text="Similar Books", font=("Helvetica", 14, "bold")).grid(row=0, column=0,
                                                                                              columnspan=5, pady=5)
    sort_books_by(books, "Similarity (decreasing)", [book])
    similar_books_calculated = books[:5]

    image_links = [x.image_url for x in similar_books_calculated]

    # Create placeholders for similar book images and titles
    for i in range(5):
        placeholder_image = load_cover_image(similar_books_frame, image_links[i - 1], 110, 150)  # Placeholder image

        # Create label with placeholder image
        image_button = tk.Button(similar_books_frame, image=placeholder_image,
                                 command=lambda idx=i: open_new_page(image_index=idx,
                                                                     the_book=similar_books_calculated))
        image_button.grid(row=1, column=i, padx=10, pady=5)

        # Create label for book title
        title_label = ttk.Label(similar_books_frame, text=similar_books_calculated[i - 1].title, wraplength=100)
        title_label.grid(row=2, column=i)

        # Keep a reference to the image to prevent garbage collection
        image_button.image = placeholder_image

    root.update_idletasks()  # Update the window to calculate widget sizes
    window_width = root.winfo_reqwidth()  # Get the requested width of the window
    window_height = root.winfo_reqheight()  # Get the requested height of the window

    # Calculate window position
    x_position = 0  # Place window at the left
    y_position = 0  # Place window at the top

    # Set window geometry
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    for x in range(13):
        root.grid_rowconfigure(x, weight=1)


def open_new_page(image_index, the_book) -> None:
    book = the_book[image_index - 1]
    create_book_page(book)


def load_cover_image(root, cover_url, width, height) -> PhotoImage:
    response = requests.get(cover_url)
    image = Image.open(BytesIO(response.content))
    image = image.resize((width, height))
    cover_image = ImageTk.PhotoImage(image)
    root.image = cover_image  # Keep a reference to prevent garbage collection
    return cover_image


def add_to_saved(book, button) -> None:
    saved_books_library.add_book(book)
    button.configure(text="Added!", style="Red.TButton", state="disabled")


def remove_from_saved(book, add_button, remove_button) -> None:
    saved_books_library.remove_book(book)
    add_button.configure(text="Add to Saved", style="TButton", state="normal")
    remove_button.configure(text="Removed!", style="Red.TButton", state="disabled")

import tkinter as tk
from tkinter import Scrollbar
from PIL import Image, ImageTk
import requests
from io import BytesIO
from bookpage import create_book_page


class ScrollingFrame(tk.Frame):
    """Creates a scrollable frame that will display books"""
    def __init__(self, master, books):
        super().__init__(master)

        self.canvas = tk.Canvas(self, width=700, height=700, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nse", padx=1, pady=1)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.scrollbar = Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame.bind("<Configure>", self.on_frame_configure)

        self.images = []
        self.labels = []

        self.host_images(books)

    def on_frame_configure(self, event) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def open_new_page(self, image_index, sorted_books_frame2) -> None:
        """Command. Creates a new book page for each book displayed"""
        book = sorted_books_frame2[image_index - 1]
        create_book_page(book)

    def host_images(self, sorted_books_frame2) -> None:
        """ Downloads and opens the image using the url links in the Book attributes. Places them on the frame"""
        # Image URLs
        image_links = [book.image_url for book in sorted_books_frame2]

        for i, link in enumerate(image_links, start=1):
            # Download image from URL using requests
            response = requests.get(link)
            # Open image using Pillow
            image = Image.open(BytesIO(response.content))
            # Resize image if necessary
            image = image.resize((110, 150))
            # Convert image to Tkinter-compatible format
            tk_image = ImageTk.PhotoImage(image)
            # Store the Tkinter image object
            self.images.append(tk_image)

            # Calculate row and column indices for placement
            row = (i - 1) // 4
            col = (i - 1) % 4

            # Create label with image and text
            label_frame = tk.Frame(self.frame)
            label_frame.grid(row=row, column=col, padx=10, pady=10)  # Adjust padding as needed

            button = tk.Button(label_frame, image=tk_image, command=lambda idx=i: self.open_new_page(idx,
                                                                                                     sorted_books_frame2
                                                                                                     ))
            button.grid(row=0, column=0)

            text_label = tk.Label(label_frame, text=f"{sorted_books_frame2[i - 1].title}", wraplength=150)
            text_label.grid(row=1, column=0)

            # Store the label
            self.labels.append(label_frame)

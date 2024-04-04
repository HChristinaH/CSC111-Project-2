"""This file creates the bottom part of the main window. Includes the filter and sorting options on the left and the books being displayed on the right

Copyright 2024 Areesha Abidi
"""
from tkinter import messagebox
from gettingdata import genres_list
import ttkbootstrap as ttk
from gettingdata import books_to_display as books
from gettingdata import tree
from scroll_frame import ScrollingFrame
from bookpage import saved_books_library


class CheckbuttonDrawer(ttk.Frame):
    """ Template for creating the filter and sorting options (in drawers)"""
    def __init__(self, master=None, title="", options=None):
        super().__init__(master)
        self.check_vars = None
        self.toggle_button = None
        self.drawer_frame = None
        self.master = master
        self.title = title
        self.options = options

        self.create_widgets()

    def create_widgets(self) -> None:
        """ Calls on the other functions to create and display the widgets"""
        self.toggle_button = ttk.Button(self, text=f"{self.title}", command=self.toggle_drawer)
        self.toggle_button.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

        self.drawer_frame = ttk.Frame(self)

        row = 1
        self.check_vars = []
        for option in self.options:
            check_var = ttk.IntVar(value=0)  # Initialize check variables to 0
            check_button = ttk.Checkbutton(self.drawer_frame, text=option, variable=check_var)
            check_button.grid(row=row, column=0, sticky="nw", padx=5, pady=2)
            self.check_vars.append(check_var)
            row += 1

    def toggle_drawer(self) -> None:
        """ Toggles the drawers un/collapsed"""
        if self.drawer_frame.winfo_ismapped():
            self.drawer_frame.grid_forget()
        else:
            self.drawer_frame.grid(row=1, column=0, sticky="nw", padx=5, pady=5)

    def get_checkbox_states(self) -> list:
        """Function to retrieve the state of each checkbox. Will return the sequence of zeros and ones used for the
        sorting and filtering function in tree.get_books_filter_sort"""
        states = [var.get() for var in self.check_vars]
        return states


class Frame2Main(ttk.Frame):
    """ Displays the sorting and filtering options in a frame created and placed on the left hand side of main window
    """
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.another_frame2 = ttk.Frame(self.master)
        self.another_frame2.grid(row=1, column=0, sticky="nsw", padx=5, pady=5)

        self.subheading = ttk.Label(self.another_frame2, text="Filters", padding=5, font="Arial, 12")
        self.subheading.grid(row=0, column=0)

        self.ratings_drawer = CheckbuttonDrawer(self.another_frame2, title="Ratings",
                                                options=["1 star", "2 star", "3 star", "4 star", "5 star"])
        self.ratings_drawer.grid(row=1, column=0, sticky="w")

        self.book_length_drawer = CheckbuttonDrawer(self.another_frame2, title="Book Length", options=["Short",
                                                                                                       "Medium",
                                                                                                       "Long"])
        self.book_length_drawer.grid(row=2, column=0, sticky="w")

        self.genres_drawer = CheckbuttonDrawer(self.another_frame2, title="Genres",
                                               options=genres_list)
        self.genres_drawer.grid(row=3, column=0, sticky="w")

        self.sort_options = ["Similarity (decreasing)", "Popularity (decreasing)", "Average rating (high to low)",
                             "Author (A-Z)", "Publication year (increasing)", "Title (A-Z)"]

        self.sort_combo = ttk.Combobox(self.another_frame2, values=self.sort_options, state="readonly")
        self.sort_combo.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        self.sort_combo.set("Sort by")

        self.apply_button = ttk.Button(self.another_frame2, text="Apply", command=self.apply_changes)
        self.apply_button.grid(row=5, column=0, sticky="ew", padx=5, pady=5)

        self.blank = ttk.Label(self, text="")
        self.blank.grid(row=0, column=1, sticky="ew", padx=100, pady=100)

        # Frame 3
        self.scrolling1 = ScrollingFrame(self, books)
        self.scrolling1.grid(row=0, column=2, sticky="nw", padx=5, pady=5)

    def apply_changes(self) -> None:
        """Command for the apply button. When the button is pressed, this will receive the sequence and call
         tree.get_books_filter_sort and then display the results on the page"""

        messagebox.showinfo("My Library Manager", "Loading, please wait")  # Takes time to load so let user know
        # Retrieve checkbox states and sorting option
        all_states = []
        all_states.extend(self.ratings_drawer.get_checkbox_states())
        all_states.extend(self.book_length_drawer.get_checkbox_states())
        all_states.extend(self.genres_drawer.get_checkbox_states())
        data = ttk.Label(self, text="")
        data.grid(row=5, column=0, sticky="w", padx=5, pady=5)

        sort_selection = self.sort_combo.get()
        data2 = ttk.Label(self, text="")
        data2.grid(row=6, column=0, sticky="w", padx=5, pady=5)

        self.blank.destroy()
        self.scrolling1.destroy()

        # Recreate ScrollingFrame instance with updated data
        new_books = tree.get_books_filter_sort(all_states, sort_selection, saved_books_library.library)
        self.scrolling1 = ScrollingFrame(self, new_books)
        self.scrolling1.grid(row=0, column=2, sticky="nw", padx=5, pady=5)

        messagebox.showinfo("My Library Manager", "Filtering Complete")

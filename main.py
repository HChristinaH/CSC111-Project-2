"""This file creates the root window and imports the frames from the files
Copyright 2024 Areesha Abidi
"""
import tkinter as tk
from main_frame1 import Frame1Main
from main_frame2 import Frame2Main


def center_window(window, width, height) -> None:
    """Helper function that will place the root window to the top center of the users screen"""
    screen_width = window.winfo_screenwidth()

    x_coordinate = (screen_width - width) // 2
    y_coordinate = 0  # Place window at the top of the screen

    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")


class MainApplication(tk.Tk):
    """ The main application that displays the program. It calls on different files that place frames within itself"""

    def __init__(self):
        super().__init__()
        self.title("My Library Manager")
        window_width = 970
        window_height = 800
        center_window(self, window_width, window_height)
        self.resizable(False, False)

        # Create instances of frames
        frame1_main = Frame1Main(self)
        frame2_main = Frame2Main(self)

        # Arrange frames within the main window
        frame1_main.grid(row=0, column=0, sticky="nsew")
        frame2_main.grid(row=1, column=0, sticky="nw")


def main():
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    main()

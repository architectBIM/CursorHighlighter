import tkinter as tk

class AppView:
    def __init__(self, master):
        self.master = master
        self.initialize_ui()

    def initialize_ui(self):
        self.master.title("Cursor Highlighter")
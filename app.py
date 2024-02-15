from tkinter import Tk
from controller import AppController


def main():
    root = Tk()
    app = AppController(root)
    app.run()

if __name__ == "__main__":
    main()

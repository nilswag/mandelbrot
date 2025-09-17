import tkinter as tk
from tkinter import Label, ttk

class Windows():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Test Application")
        self.root.geometry("600x600")
        self.root.minsize(600,600)
        self.root.maxsize(600,600)

        Label(self.root,text="Hello World").pack()

        self.root.mainloop()

if __name__ == "__main__":
    testObj = Windows()
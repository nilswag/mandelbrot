import tkinter as tk
from tkinter import colorchooser

from PIL import Image, ImageTk

class ColorPicker(tk.Frame):
    def __init__(self, master, text, color=(0, 0, 0)):
        super().__init__(master)

        self._rgb = color
        self._hex = "#{:02x}{:02x}{:02x}".format(*color)

        self.frame = tk.Frame(self, width=20, height=20, background=self._hex)
        self.frame.pack(side="left")

        self.button = tk.Button(self, text=text, command=self.click)
        self.button.pack(side="left")

    def click(self):
        self._rgb, self._hex = colorchooser.askcolor()
        self.frame.configure(background=self.hex)

    @property
    def rgb(self):
        return self._rgb
    
    @property
    def hex(self):
        return self._hex

class CatalogEntry(tk.Frame):
    def __init__(self, master, path, click_callback):
        super().__init__(master)
        self.click_callback = click_callback

        self.path = path

        image = Image.open(path)
        image = image.resize((100, 100))
        self.ref = ImageTk.PhotoImage(image)

        self.image_label = tk.Label(self, background="lightgray", image=self.ref)
        self.image_label.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        label = tk.Label(self, text=path)
        label.pack(side="top")

        self.image_label.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        self.click_callback(self)

    def set_selected(self, selected):
        color = "lightgray"
        if selected:
            color = "lightblue"
        
        self.image_label.configure(bg=color)
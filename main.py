import colorsys
import random
import tkinter as tk
from tkinter import Button, Entry, Label, StringVar, ttk

from PIL.ImageTk import PhotoImage
from PIL import Image, ImageTk

from math import sqrt

import numpy as np


class App:
    def __init__(self):
        # Initieer tkinter and geef de window een titel
        self.root = tk.Tk()
        self.root.title("Mandelbrot")

        # Maak de window niet resizable
        self.root.resizable(False, False)

        Label(self.root, text="Midden x").pack()
        self.midden_x_var = StringVar()
        Entry(self.root, textvariable=self.midden_x_var).pack()

        Label(self.root, text="Midden y").pack()
        self.midden_y_var = StringVar()
        Entry(self.root, textvariable=self.midden_y_var).pack()

        Label(self.root, text="Schaal").pack()
        self.schaal_var = StringVar()
        Entry(self.root, textvariable=self.schaal_var).pack()

        Label(self.root, text="Max aantal").pack()
        self.max_aantal_var = StringVar()
        Entry(self.root, textvariable=self.max_aantal_var).pack()

        Button(self.root, text="Go", command=self.get_input_values).pack()

        # self.image = tk.Image(self.root)

        self.error_label = Label(self.root, text="")

        self.canvas = Label(self.root)

        self.root.mainloop()

    def get_input_values(self):
        try:

            a = float(self.midden_x_var.get())
            b = float(self.midden_y_var.get())
            schaal = float(self.schaal_var.get())
            max_aantal = int(self.max_aantal_var.get())
            self.error_label.pack_forget()
        except Exception as e:
            print(e)
            self.error_label.configure(text=f"Error: {e}")
            self.error_label.pack()

        print(f"Midden x: {self.midden_x_var.get()}")
        print(f"Midden y: {self.midden_y_var.get()}")
        print(f"Schaal: {self.schaal_var.get()}")
        print(f"Max Aantal: {self.max_aantal_var.get()}")

        WIDTH = 500
        image = Image.new(mode="RGBA", size=(WIDTH, WIDTH))
        pixels = image.load()

        x = 0
        y = 0

        multiplier = a  # <- Dit is de x-as verschuiving 0.5 is 0
        divider = schaal  # <- Zoom level aka schaal 1 dan is die gecentreerd
        verschuiving_y = b

        for x in range(WIDTH):
            for y in range(WIDTH):
                mandel_values = self.mandelbrot(
                    (x - (multiplier * WIDTH)) / (WIDTH / divider),
                    ((y - (WIDTH / divider)) / (WIDTH / divider) - verschuiving_y),
                    max_aantal,
                )
                pixels[x, y] = mandel_values

        # image.save()
        image.show()

    def mandelbrot(self, x, y, max_recursion):
        c = complex(x, y)
        z = 0
        for i in range(1, max_recursion):
            if abs(z) > 2:
                if i % 2 == 0:
                    return (255, 255, 255)
                else:
                    return (0, 0, 0)
            z = z * z + c

        # print("Max recursion reached")
        return (255, 0, 255)


if __name__ == "__main__":
    App()

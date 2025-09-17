import colorsys
import copy
import numpy as np
import tkinter as tk
from tkinter import Button, Entry, Label, StringVar, ttk

from PIL.ImageTk import PhotoImage
from PIL import Image, ImageTk

from math import sqrt

class App():
    def __init__(self):
        # Initieer tkinter and geef de window een titel
        self.root = tk.Tk()
        self.root.title("Mandelbrot")

        # Maak de window niet resizable
        self.root.resizable(False, False)

        Label(self.root, text="Midden x").pack()
        self.midden_x_var = StringVar()
        Entry(self.root, textvariable = self.midden_x_var).pack()

        Label(self.root, text = "Midden y").pack()
        self.midden_y_var = StringVar()
        Entry(self.root, textvariable = self.midden_y_var).pack()

        Label(self.root, text = "Schaal").pack()
        self.schaal_var = StringVar()
        Entry(self.root, textvariable = self.schaal_var).pack()

        Label(self.root, text = "Max aantal").pack()
        self.max_aantal_var = StringVar()
        Entry(self.root, textvariable = self.max_aantal_var).pack()

        Button(self.root, text="Go", command = self.get_input_values).pack()

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
        

        for x in range(image.size[0]):
            for y in range(image.size[1]):
                mandel_values = self.mandelbrot((x - (0.75 * WIDTH)) / (WIDTH / 4),
                                      (y - (WIDTH / 4)) / (WIDTH / 4), max_aantal)
                # print(x, y, pixels[x, y], mandel_values)
                pixels[x, y] = mandel_values
                # pixels[x, y] = (mandel_values, mandel_values, mandel_values, 0)

        image.show()

    def rgb_conv(self, i):
        color = 255 * np.array(colorsys.hsv_to_rgb(i / 255.0, 1.0, 0.5))
        return tuple(color.astype(int))

    def mandelbrot(self, x, y, max_recursion):
        c0 = complex(x, y)
        c = 0
        for i in range(1, max_recursion):
            if abs(c) > 2:
                return self.rgb_conv(i)
            c = c * c + c0
        return (0, 0, 0)


if __name__ == "__main__":
    App()
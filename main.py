import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# a = x coordinaat die getransformeerd wordt
# b = y coordinaat die getransformeerd wordt
# x = x coordinaat van middenpunt van mandelbroot
# y = y coordinaat van middenpunt van mandelbroot
def mandelbrot(x, y, max_i):
    a, b = 0, 0
    for i in range(max_i):
        a_new = a * a - b * b + x
        b_new = 2 * a * b + y
        a, b = a_new, b_new
        if a * a + b * b > 4:
            return i + 1
    return max_i

def map(v, d1, d2):
    a, b = d1
    c, d = d2
    return c + (v - a) * (d - c) / (b - a)

class App(tk.Frame):
    def __init__(self, master: tk.Tk):
        # Programma instellingen en aanroep naar parent
        super().__init__(master)
        self.pack(fill="both", expand=True)
        master.title("Mandelbrot")
        master.resizable(False, False)

        # Layout definities
        input_frame = tk.Frame(self)
        input_frame.pack(side="top", pady=20)

        labels = ["Midden X: ", "Midden Y: ", "Zoom: ", "Maximum aantal: "]
        entries = []
        self.vars = []
        for i, text in enumerate(labels):
            var = tk.StringVar()
            var.set(0)
            self.vars.append(var)

            tk.Label(input_frame, text=text).grid(row=i, column=0)
            entry = tk.Entry(input_frame, textvariable=var)
            entry.grid(row=i, column=1)

            entries.append(entry)
        self.go_btn = tk.Button(input_frame, command=self.go, text="Go!", width=4)
        self.go_btn.grid(row=3, column=2)

        self.vars[2].set(1.0)
        self.vars[3].set(100)

        # Plaatje
        self.image_label = tk.Label(self)
        self.image_label.pack(fill="both", expand=True, side="top")

        self.image = None

        self.image_label.bind("<Button-1>", self.left_click)
        self.image_label.bind("<Button-3>", self.right_click)

    def assert_inputs(self):
        vars = []

        for var in self.vars:
            try:
                input = float(var.get())
            except:
                messagebox.showerror("Invalid input", f"All inputs must be numeric, {var.get()} is not numeric!")

    def click(self, dir, x, y):
        zoom = float(self.vars[2].get())
        self.vars[2].set(zoom + dir * 0.25)

        self.vars[0].set(map(x, [0, self.image.width - 1], [-2 / zoom, 2 / zoom]))
        self.vars[1].set(map(y, [0, self.image.height - 1], [2 / zoom, -2 / zoom]))

        self.go()

    def left_click(self, event):
        self.click(1, event.x, event.y)

    def right_click(self, event):
        self.click(-1, event.x, event.y)

    def go(self):
        self.assert_inputs()

        midden_x = float(self.vars[0].get())
        midden_y = float(self.vars[1].get())
        zoom = float(self.vars[2].get())
        max_aantal = int(self.vars[3].get())

        self.image = Image.new("RGBA", (self.image_label.winfo_width(), self.image_label.winfo_height()), "black")

        for px in range(self.image.width):
            for py in range(self.image.height):
                a = midden_x - map(px, [0, self.image.width - 1], [-2 / zoom, 2 / zoom])
                b = midden_y - map(py, [0, self.image.height - 1], [-2 / zoom, 2 / zoom])
                i = mandelbrot(a, b, max_aantal)
                
                self.image.putpixel((px, py), (0, 255 % i * 20, 0))

        self.ref = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.ref)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x600")
    app = App(root)
    root.mainloop()
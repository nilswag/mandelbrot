import tkinter as tk
from PIL import Image, ImageTk

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

        labels = ["Midden X: ", "Midden Y: ", "Schaal: ", "Maximum aantal: "]
        self.entries = []
        for i, text in enumerate(labels):
            tk.Label(input_frame, text=text).grid(row=i, column=0)
            entry = tk.Entry(input_frame)
            entry.grid(row=i, column=1)

            self.entries.append(entry)
        self.go_btn = tk.Button(input_frame, command=self.go, text="Go!", width=4)
        self.go_btn.grid(row=3, column=2)

    def go(self):
        print("Hello")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    app = App(root)
    root.mainloop()
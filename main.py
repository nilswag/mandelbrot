import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox

from math import log, sqrt

from util import *
from widgets import *

class Catalog(tk.Toplevel):
    def __init__(self, master, selected_callback):
        super().__init__(master)

        self.selected_callback = selected_callback

        self.datasets = {
            # Path van het plaatje (midden_x, midden_y, zoom, max_aantal)
            "images/1.png": (0, 0, 1.0, 100),
            "images/2.png": (0, 0, 1.0, 100),
            "images/3.png": (0, 0, 1.0, 100),
            "images/4.png": (0, 0, 1.0, 100)
        }

        entry_width = 140
        entry_height = 180

        self.entries = []
        self.selected = None

        for i, key in enumerate(self.datasets.keys()):
            entry = CatalogEntry(self, key, self.select_entry)
            entry.grid(row=0, column=i, padx=5, pady=10)
            self.entries.append(entry)

        tk.Button(self, text="Load", command=lambda: self.selected_callback(self), width=10).grid(row=1, column=3)

        self.geometry(f"{len(self.entries) * entry_width}x{entry_height + 30}")
        self.resizable(False, False)

    def select_entry(self, entry):
        if self.selected:
            self.selected.set_selected(False)
        
        entry.set_selected(True)
        self.selected = entry

class App(tk.Frame):
    def __init__(self, master):
        # Programma instellingen en aanroep naar parent
        super().__init__(master)
        self.pack(fill="both", expand=True)
        master.title("Mandelbrot")
        master.resizable(False, False)

        input_frame = tk.Frame(self)
        input_frame.pack(side="top", pady=20)

        # Maak een dictionary met als key een leesbare naam en met als waarde te tekst van de label
        labels = {"midden_x": "Midden X: ", "midden_y": "Midden Y: ", "zoom": "Zoom: ", "max_aantal": "Maximum aantal: "}
        self.vars = {}
        # Hierdoor krijgen wij elementen in de vorm van i, de key van de tekst
        for i, key in enumerate(labels):
            var = tk.StringVar()
            var.set(0)
            self.vars[key] = var
            # Hiermee zetten wij alle keys gelijk aan de input variabele

            # Door i te gebruiken kunnen wij de entries op een nette manier sorteren in de layout
            tk.Label(input_frame, text=labels[key]).grid(row=i, column=0)
            entry = tk.Entry(input_frame, textvariable=var)
            entry.grid(row=i, column=1)
            # Wij hoeven verder niks meer met de entries te doen gezien de entries zelf een reference hebben naar de stringvars, deze hebben wij wel opgeslagen

        # Zet een aantal default waardes
        self.vars["zoom"].set(1.0)
        self.vars["max_aantal"].set(100)

        self.image_label = tk.Label(self)
        self.image_label.pack(fill="both", expand=True, side="top", padx=10, pady=10)

        self.image_label.bind("<Button-1>", self.left_click)
        self.image_label.bind("<Button-3>", self.right_click)

        # Knop gedoe
        btn_frame = tk.Frame(input_frame)
        btn_frame.grid(row=4, column=1)

        self.color0 = ColorPicker(btn_frame, "Kleur 1", color=(180, 0, 0))
        self.color0.pack(side="left", padx=3)

        self.color1 = ColorPicker(btn_frame, "Kleur 2", color=(255, 220, 0))
        self.color1.pack(side="left", padx=3)

        self.backgr = ColorPicker(btn_frame, "Achtergrond kleur", color=(0, 0, 0))
        self.backgr.pack(side="left", padx=3)

        self.go_btn = tk.Button(btn_frame, command=self.go, text="Go!", width=4)
        self.go_btn.pack(side="left", padx=3)

        self.examples_btn = tk.Button(btn_frame, command=lambda: Catalog(self, self.examples_callback), text="Examples")
        self.examples_btn.pack(side="left", padx=3)

    def examples_callback(self, catalog):
        catalog.destroy()
        if not catalog.selected:
            return
        
        selected = catalog.datasets[catalog.selected.path]
        
        self.vars["midden_x"].set(selected[0])
        self.vars["midden_y"].set(selected[1])
        self.vars["zoom"].set(selected[2])
        self.vars["max_aantal"].set(selected[3])

    def assert_inputs(self):
        vars = []

        # Dit checks dat daadwerkelijk alle waardes getallen zijn anders kun je niet verder
        for var in self.vars.values():
            try:
                input = float(var.get())
            except:
                # Als er een niet getal in de inputs staat komt er een popup
                messagebox.showerror("Invalid input", f"All inputs must be numeric, {var.get()} is not numeric!")
                return False
        return True

    def click(self, left, x, y):
        if not self.assert_inputs():
            return

        # Verander de zoom op basis van of er in- of uitgezoomed wordt
        zoom = self.vars["zoom"]
        midden_x = self.vars["midden_x"]
        midden_y = self.vars["midden_y"]

        if left:
            zoom.set(float(zoom.get()) * 1.25)
        else:
            zoom.set(float(zoom.get()) / 1.25)

        cx = self.image.width / 2 # Bereken x coordinaat van midden van scherm
        cy = self.image.height / 2 # Bereken y coordinaat van midden van scherm

        # Verschil van muis positie tot middenpunt van scherm
        dx = x - cx
        dy = y - cy

        # Gezien we op een punt op het complexe vak gecenteerd staan moeten wij de muis vanuit het midden van ons scherm zien te mappen naar het complexe vak
        # Hiermee berekenen wij het verschil vanuit het midden wat wij kunnen toevoegen aan het verschuiven van het figuur
        midden_dx = map(dx, [-cx, cx], [-2 / float(zoom.get()), 2 / float(zoom.get())])
        midden_dy = map(dy, [-cy, cy], [2 / float(zoom.get()), -2 / float(zoom.get())])

        midden_x.set(float(midden_x.get()) + midden_dx)
        midden_y.set(float(midden_y.get()) + midden_dy)

        self.go()

    def left_click(self, event):
        self.click(True, event.x, event.y)

    def right_click(self, event):
        self.click(False, event.x, event.y)

    def go(self):
        if not self.assert_inputs():
            return

        # Zet alle references van de inputs in locale variabelen
        midden_x = float(self.vars["midden_x"].get())
        midden_y = float(self.vars["midden_y"].get())
        zoom = float(self.vars["zoom"].get())
        max_aantal = int(self.vars["max_aantal"].get())

        # Maak het plaatje aan (dit is persistant gezien het onderdeel is van het app object)
        self.image = Image.new("RGBA", (self.image_label.winfo_width(), self.image_label.winfo_height()), "black")

        # Loop door alle pixels heen van het plaatje
        for px in range(self.image.width):
            for py in range(self.image.height):
                # Hier komt de map functie van pas, we mappen alle pixels naar het complexe vlak, hierdoor is het mandelgetal ook altijd in hoge resolutie
                a = midden_x + map(px, [0, self.image.width - 1], [-2 / zoom, 2 / zoom])
                b = midden_y + map(py, [0, self.image.height - 1], [2 / zoom, -2 / zoom])
                i, r2 = mandelbrot(a, b, max_aantal)
                i *= 7

                # Hier worden de mooie kleuren gezet
                color = (0, 0, 0)
                if i >= max_aantal:
                    # Als het max aantal iterations is bereikt gebruik achtergrond kleur
                    color = self.backgr.rgb
                else:
                    # Formule is van internet geplukt, z_n = sqrt(r^2)
                    # dus log(z_n) = log(sqrt(r^2)) = 0.5 * log(r^2)
                    v = i + 1 - log(sqrt(r2)) / log(2)  # smooth maken
                    t = v / max_aantal                  # normalizeren
                    color = lerp_color(self.color0.rgb, self.color1.rgb, t)
                
                self.image.putpixel((px, py), color)

        # Het gegenereerde plaatje wordt in het window gezet
        self.ref = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.ref)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x600")
    app = App(root)
    root.mainloop()
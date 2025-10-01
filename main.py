import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, colorchooser

from math import log, sqrt

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

# a = x coordinaat die getransformeerd wordt
# b = y coordinaat die getransformeerd wordt
# x = x coordinaat van middenpunt van mandelbroot
# y = y coordinaat van middenpunt van mandelbroot
# max_i = aantal iterations voordat het algoritme stops
# a0 en b0 = de start waardes van het mandelfiguur, nuttig voor de catalogus
def mandelbrot(x, y, max_i, a0=0, b0=0):
    a, b = a0, b0
    for i in range(max_i):
        a_new = a * a - b * b + x
        b_new = 2 * a * b + y
        a, b = a_new, b_new
        r2 = a * a + b * b
        if r2 > 4:
            return i + 1, sqrt(r2)
    return max_i, sqrt(a * a + b * b)

# Lineaire mapping van de variable v van het domein d1 naar d2
def map(v, d1, d2):
    a, b = d1
    c, d = d2
    return c + (v - a) * (d - c) / (b - a)

# Op basis van t (t zit tussen 0 en 1) verander gelijkmatig de kleur
def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

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
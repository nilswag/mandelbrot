from math import sqrt

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
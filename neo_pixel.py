# -*- coding: utf-8 -*-
from esp import neopixel_write


class NeoPixel:
    """ Fixed version from MicroPython """
    def __init__(self, pin, n):
        self.pin = pin
        self.n = n
        self.buf = bytearray(n * 3)
        self.pin.init(pin.OUT)

    @staticmethod
    def hsv_to_rgb(h, s, v):
        """ From colorsys.py """
        if s == 0.0:
            return v, v, v
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        if i == 0:
            return v, t, p
        if i == 1:
            return q, v, p
        if i == 2:
            return p, v, t
        if i == 3:
            return p, q, v
        if i == 4:
            return t, p, v
        if i == 5:
            return v, p, q

    def __setitem__(self, index, val):
        print('__setitem__()')
        r, g, b = val
        self.buf[index * 3] = g
        self.buf[index * 3 + 1] = r
        self.buf[index * 3 + 2] = b

    def __getitem__(self, index):
        i = index * 3
        return self.buf[i + 1], self.buf[i], self.buf[i + 2]

    def fill_rgb(self, color):
        r, g, b = color
        for i in range(len(self.buf) / 3):
            self.buf[i * 3] = g
            self.buf[i * 3 + 1] = r
            self.buf[i * 3 + 2] = b

    def fill_hsv(self, color):
        """ """
        h, s, v = color
        r, g, b = NeoPixel.hsv_to_rgb(h, s, v)
        self.fill_rgb((int(r * 255), int(g * 255), int(b * 255)))

    def write(self):
        neopixel_write(self.pin, self.buf, True)

    def set_rainbow(self):
        for x in range(self.n):
            r, g, b = NeoPixel.hsv_to_rgb(x * 1.0 / self.n, 1, 1)
            self[x] = (int(r * 255), int(g * 255), int(b * 255))
        self.write()

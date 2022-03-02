##!/usr/bin/env python
"""PanZoomLab - A code lab to explore panning and zooming in Pyxel."""

from random import randint
import pyxel

class App:

    def __init__(self):
        self.palette = [0x000000, 0x1B2119, 0x232C21, 0x292C2D,
                        0x2E3044, 0x3A503C, 0x454758, 0x556F57,
                        0x626573, 0x67A9C2, 0x7AA07F, 0x85878B,
                        0xACAFAF, 0xCACDCD, 0xE6E8E7, 0xFFFFFF]

        pyxel.init(320, 240, title="PanZoomLab", fps=60)
        pyxel.colors.from_list(self.palette)
        pyxel.image(1).load(0, 0, "../3310-256.png")

        self.zoom = False
        self.mag = 2
        self.xOff = 0
        self.yOff = 0

        self.normal = pyxel.Image(320, 240)
        self.normal.cls(5)
        self.normal.blt(0, 0, 1, 0, 0, 160, 120, 10)
        self.normal.blt(160, 0, 1, 0, 0, -160, 120, 10)
        self.normal.blt(0, 120, 1, 0, 0, 160, -120, 10)
        self.normal.blt(160, 120, 1, 0, 0, -160, -120, 10)
        self.normal.text(75, 120, f"[PAGE UP / DOWN]: ZOOM +/- [J] ZOOM On/Off", 4)

        self.buildZoom()

        pyxel.run(self.update, self.draw)

    def draw(self):
        if self.mag > 1 and self.zoom:
            pyxel.camera(self.xOff, self.yOff)
            pyxel.blt(0, 0, self.zoomed, 0, 0, 320*self.mag, 240*self.mag)
        else:
            pyxel.blt(0, 0, self.normal, 0, 0, 320, 240)

        pyxel.camera()
        pyxel.text(0, 18, f"X{self.mag} ({pyxel.mouse_x}, {pyxel.mouse_y}) {self.xOff}, {self.yOff}", 15)
        pyxel.pset(pyxel.mouse_x, pyxel.mouse_y, 9)

    def update(self):
        if pyxel.btnp(pyxel.KEY_J):
            self.zoom = not self.zoom

        if pyxel.btnp(pyxel.KEY_PAGEUP):
            self.zoom = True
            self.mag += 1
            self.buildZoom()

        if pyxel.btnp(pyxel.KEY_PAGEDOWN):
            self.zoom = True
            self.mag -= 1
            if self.mag < 1:
                self.mag = 1
            self.buildZoom()

        if pyxel.mouse_x > 0 and pyxel.mouse_x < 320:
            ratio = pyxel.mouse_x / 320
            self.xOff = 320 * ratio * self.mag
            if self.xOff > 320 * (self.mag - 1):
                self.xOff = 320 * (self.mag - 1)

        if pyxel.mouse_y > 0 and pyxel.mouse_y < 240:
            ratio = pyxel.mouse_y / 240
            self.yOff = 240 * ratio * self.mag
            if self.yOff > 240 * (self.mag - 1):
                self.yOff = 240 * (self.mag - 1)

    def buildZoom(self):
        print(f"Rebuilding zoom x{self.mag} ({320*self.mag}, {240*self.mag})")
        self.zoomed = pyxel.Image(320*self.mag, 240*self.mag)
        for y in range(240):
            for x in range(320):
                self.zoomed.rect(x * self.mag,
                                 y * self.mag,
                                 self.mag,
                                 self.mag,
                                 self.normal.pget(x, y))


App()

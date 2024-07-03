import numpy as np
import tkinter as tk
import fourier_svg

class FourierCanvas(tk.Canvas):
    TICKS = 1, 0.2, 0.4
    FONT_SIZE = 9

    def __init__(self, root, size, precision):
        super().__init__(root, width=size, height=size, bg='white')
        self.SIZE = size * (1 + 1j)
        self.PRECISION = precision

        self.grid(column=0, row=0, columnspan=2)

        self.dim = self.SIZE / (self.TICKS[0]+self.TICKS[1]) / 2
        self.xs = np.arange(0, 1+self.PRECISION, self.PRECISION)
        self.ys = [np.exp(2j*np.pi*x) for x in self.xs]

        self.kolleg_points = fourier_svg.get_svg_points('kolleg_logo.svg', 1000, self.TICKS[0]*1.9)
        self.bind('<B1-Motion>', self.on_drag)

        self.draw_grid()
        self.update_ys()
        # self.draw_svg()

    def on_drag(self, evt):
        pos = self.transform_pos_inverse(evt.x + evt.y * 1j)
        angle = np.arctan2(pos.imag, pos.real)
        self.ys[int(angle / np.pi / 2 / self.PRECISION)] = np.exp(1j*angle) * np.sqrt(pos * pos.conjugate())
        self.update_ys()

    def update_ys(self):
        self.delete('ys')
        dot_size = 10 * (1+1j)
        for c in self.ys:
            ap = self.transform_pos(c)
            self.create_oval(
                fourier_svg.pos_to_tuple(ap - dot_size/2),
                fourier_svg.pos_to_tuple(ap + dot_size/2),
                tags='ys', fill='blue'
            )

    def transform_pos(self, p: complex) -> complex:
        return p.real * self.dim.real - p.imag * self.dim.imag * 1j + self.SIZE/2

    def transform_pos_inverse(self, p: complex) -> complex:
        pp = p - self.SIZE/2
        return pp.real / self.dim.real - pp.imag / self.dim.real * 1j

    def polygon_points(self, points: list[complex]) -> list[tuple[float]]:
        return [fourier_svg.pos_to_tuple(self.transform_pos(p)) for p in points]

    def draw_grid(self, **kwargs):
        tl = self.TICKS[1] * 0.2
        self.draw_arrow(self.SIZE.imag * 0.5j, 0, self.SIZE.real, ab=True, tl=20, tags='coorsys')
        self.draw_arrow(self.SIZE.real * 0.5 + self.SIZE.imag * 1j, -np.pi / 2, self.SIZE.imag, ab=True, tl=20, tags='coorsys')
        self.create_text((self.SIZE.real/2 + 20, 10), text='Re', font=f'tkDefaeultFont {int(self.FONT_SIZE*1.5)}', anchor='w')
        self.create_text((self.SIZE.real, self.SIZE.imag/2 + 10), text='Im', font=f'tkDefaeultFont {int(self.FONT_SIZE*1.5)}', anchor='ne')
        for ax in range(4):
            for t in np.arange(0, self.TICKS[0] + self.TICKS[1], self.TICKS[1]):
                if t > 0:
                    lines = [[t - tl * 1j, t + tl * 1j], [t - self.TICKS[0] * 1j, t + self.TICKS[0] * 1j]]
                    lines = [[fourier_svg.pos_to_tuple(self.transform_pos(1j ** ax * p)) for p in line] for line in lines]
                    self.create_line(*lines[1], fill='#bbb', width=0.1, tags='coorsys')
                    self.create_line(*lines[0], fill='black', width=3, tags='coorsys')
                    if np.isclose(t % self.TICKS[2], 0) or t == self.TICKS[0]:
                        lb = ('–' if ax > 1 else '') + str(round(t, 1)) + ('i' if ax % 2 == 1 else '')
                        lp = fourier_svg.pos_to_tuple(self.transform_pos(1j ** ax * (t - tl * len(lb) * 0.75j)))
                        self.create_text(lp, text=lb, font=f'tkDefaeultFont {self.FONT_SIZE}', anchor='center')


    def draw_svg(self):
        self.create_polygon(*self.polygon_points(self.kolleg_points), fill='blue')

    def draw_arrow(self, p: complex, a: float, l: float, **kwargs):
        lw, tl, aa, fl = kwargs.get('lw', 2), kwargs.get('tl', self.TICKS[0] * 0.05), kwargs.get('aa', np.pi / 8), kwargs.get('fl', 'black')
        line = [p, p + l*np.exp(a*1j)]
        tip = [line[1], line[1] - tl*np.exp((a+aa)*1j), line[1] - tl*np.exp((a-aa)*1j)]
        if not kwargs.get('ab', False):
            line = [self.transform_pos(p) for p in line]
            tip = [self.transform_pos(p) for p in tip]
        tip = [(t.real, t.imag) for t in tip]

        self.create_line(line[0].real, line[0].imag, line[1].real, line[1].imag, fill=fl, width=lw)
        self.create_polygon(*tip, fill=fl)

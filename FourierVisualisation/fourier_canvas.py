import numpy as np
import tkinter as tk

import pylab as p

import fourier_math

class FourierCanvas(tk.Canvas):
    TICKS = 1.4, 0.2, 0.4
    FONT_SIZE = 6

    def __init__(self, root, size, precision):
        super().__init__(root, width=size, height=size, bg='white')
        self.SIZE = size * (1 + 1j)
        self.PRECISION = precision
        self.dim = self.SIZE / (self.TICKS[0]+self.TICKS[1]) / 2
        self.draw_grid()

    def transform_pos(self, p: complex) -> complex:
        return p.real * self.dim.real - p.imag * self.dim.imag * 1j + self.SIZE/2

    def transform_pos_inverse(self, p: complex) -> complex:
        pp = p - self.SIZE/2
        return pp.real / self.dim.real - pp.imag / self.dim.real * 1j

    def polygon_points(self, points: list[complex]) -> list[tuple[float]]:
        return [fourier_math.pos_to_tuple(self.transform_pos(p)) for p in points]

    def draw_grid(self, **kwargs):
        tl = self.TICKS[1] * 0.2
        self.draw_arrow(self.SIZE.imag * 0.5j, self.SIZE.real, ab=True, tl=20, tags='coorsys')
        self.draw_arrow(self.SIZE.real * 0.5 + self.SIZE.imag * 1j, -self.SIZE.imag*1j, ab=True, tl=20, tags='coorsys')
        self.create_text((self.SIZE.real/2 + 20, 10), text='Im', font=f'tkDefaeultFont {int(self.FONT_SIZE*1.5)}', anchor='w')
        self.create_text((self.SIZE.real, self.SIZE.imag/2 + 10), text='Re', font=f'tkDefaeultFont {int(self.FONT_SIZE*1.5)}', anchor='ne')
        for ax in range(4):
            for t in np.arange(0, self.TICKS[0] + self.TICKS[1], self.TICKS[1]):
                if t > 0:
                    lines = [[t - tl * 1j, t + tl * 1j], [t - self.TICKS[0] * 1j, t + self.TICKS[0] * 1j]]
                    lines = [[fourier_math.pos_to_tuple(self.transform_pos(1j ** ax * p)) for p in line] for line in lines]
                    self.create_line(*lines[1], fill='#bbb', width=0.1, tags='coorsys')
                    self.create_line(*lines[0], fill='black', width=3, tags='coorsys')
                    if np.isclose(t % self.TICKS[2], 0):
                        lb = ('–' if ax > 1 else '') + str(round(t, 1)) + ('i' if ax % 2 == 1 else '')
                        lp = fourier_math.pos_to_tuple(self.transform_pos(1j ** ax * (t - tl * len(lb) * 0.75j)))
                        self.create_text(lp, text=lb, font=f'tkDefaeultFont {self.FONT_SIZE}', anchor='center')


    def draw_svg(self):
        self.create_polygon(*self.polygon_points(self.kolleg_points), fill='blue')

    def draw_arrow(self, p: complex, d: complex, **kwargs):
        a, line = np.arctan2(d.imag, d.real), [p, p + d]
        lw, tl, aa, fl = kwargs.get('lw', 2), kwargs.get('tl', self.TICKS[0] * 0.05), kwargs.get('aa', np.pi / 8), kwargs.get('fl', 'black')
        tip = [line[1], line[1] - tl*np.exp((a+aa)*1j), line[1] - tl*np.exp((a-aa)*1j)]
        if not kwargs.get('ab', False):
            line = [self.transform_pos(p) for p in line]
            tip = [self.transform_pos(p) for p in tip]
        tip = [(t.real, t.imag) for t in tip]

        self.create_line(line[0].real, line[0].imag, line[1].real, line[1].imag, fill=fl, width=lw, tags=kwargs.get('tags', []))
        self.create_polygon(*tip, fill=fl, tags=kwargs.get('tags', []))

    def update_points(self, ys):
        self.delete('ys_points')
        for i, z in enumerate(ys):
            pos = self.transform_pos(z)
            ps = 5 * (1+1j) * (1 if i < len(ys)-1 else 4)
            self.create_oval(
                fourier_math.pos_to_tuple(pos - ps/2),
                fourier_math.pos_to_tuple(pos + ps/2),
                outline=None if i < len(ys) - 1 else 'black',
                fill='blue' if i < len(ys)-1 else 'red', tags='ys_points'
            )

    def update_pointers(self, pointers, t: float):
        self.delete('pointers')

        if len(pointers) > 1:
            path = sum(pointers)
            last_pos = self.transform_pos(path[0])
            for z in path[1:int(len(path)*t+1)]:
                next_pos = self.transform_pos(z)
                self.create_line(
                    fourier_math.pos_to_tuple(last_pos),
                    fourier_math.pos_to_tuple(next_pos),
                    fill='red', width=3, tags='pointers'
                )
                last_pos = next_pos

        if len(pointers) > 0:
            last_pos, approx_n, ind = 0, len(pointers) // 2, int(t*len(pointers[0]))
            max_length = max([np.sqrt(sp[ind]*sp[ind].conjugate()) for sp in pointers])
            for nn in range(approx_n+1):
                for n in [nn] if nn == 0 else [nn, -nn]:
                    delta = pointers[n+approx_n][ind]
                    length = np.sqrt(delta * delta.conjugate())
                    size_f = 0.3 + 0.7*length / max_length
                    self.draw_arrow(
                        last_pos, delta, lw=int(3*size_f),
                        tl=self.TICKS[0] * 0.05 * size_f, tags='pointers'
                    )
                    self.create_oval(
                        fourier_math.pos_to_tuple(self.transform_pos(last_pos-length*(1+1j))),
                        fourier_math.pos_to_tuple(self.transform_pos(last_pos+length*(1+1j))),
                        fill='', outline='orange', width=int(3*size_f), tags='pointers'
                    )
                    last_pos += delta

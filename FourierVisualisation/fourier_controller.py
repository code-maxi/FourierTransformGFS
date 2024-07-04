import threading
import numpy as np
import tkinter as tk
import fourier_canvas
import fourier_math


class FourierController(tk.Tk):
    MAX_N = 100
    SIZE = 900
    PRECISION = 1000
    SLIDER_NAMES = ['Parameter', 'Approximation N', 'Zeit t', 'Geschwindigkeit']
    SLIDER_CONF = [(0, 1, 1/PRECISION, 0), (1, MAX_N, 1, 1), (0, 1, 1 / PRECISION, 0), (0, 1, 1 / PRECISION, 0.5)]
    RADIO_NAMES = ['sin', 'rect', 'lin', 'square', 'unknown']
    SPEED = 5/PRECISION, 1/PRECISION
    KOLLEG_SIZE = 2

    def __init__(self):
        super().__init__()
        self.title('Komplexe Fourierreihe')

        self.canvas = fourier_canvas.FourierCanvas(self, self.SIZE, self.PRECISION)
        self.canvas.grid(column=0, row=0, rowspan=len(self.SLIDER_NAMES)+3, padx=30, pady=15)

        self.slider_values = [tk.DoubleVar(value=self.SLIDER_CONF[i][3]) for i in range(len(self.SLIDER_NAMES))]
        self.slider_labels = [tk.Label(self, text=n, anchor='e') for n in (self.SLIDER_NAMES + ['Funktion'])]

        self.sliders = [tk.Scale(
            self, length=int(self.SIZE * 0.6),
            resolution=self.SLIDER_CONF[i][2],
            from_=self.SLIDER_CONF[i][0],
            to=self.SLIDER_CONF[i][1], orient='horizontal',
            variable=self.slider_values[i]
        ) for i in range(len(self.SLIDER_NAMES))]

        for var in self.slider_values: var.trace_add('write', self.slider_changed)

        for i, label in enumerate(self.slider_labels):
            label.grid(sticky='w', column=1, row=i + 1, padx=30)
            if i < len(self.SLIDER_NAMES):
                self.sliders[i].grid(column=2, row=i+1, columnspan=len(self.RADIO_NAMES), padx=30)

        self.selected_radio = tk.StringVar(value=self.RADIO_NAMES[1])
        self.radio_buttons = [tk.Radiobutton(self, text=n, value=n, variable=self.selected_radio, command=self.on_radio) for n in self.RADIO_NAMES]
        for i, rb in enumerate(self.radio_buttons): rb.grid(column=2+i, row=1+len(self.SLIDER_NAMES))

        self.is_animation = tk.BooleanVar(value=False)
        self.animation_event = threading.Event()

        self.animation_on = tk.Checkbutton(self, text='Animation', onvalue=True, offvalue=False, variable=self.is_animation, command=self.on_animation)
        self.animation_on.grid(row=len(self.SLIDER_NAMES)+2, column=1, columnspan=len(self.RADIO_NAMES)+1)

        self.function_points = [self.points_of(n) for n in self.RADIO_NAMES]
        self.function_coefficients = [fourier_math.find_coefficients(points, self.MAX_N) for points in self.function_points]

        self.fourier_parts = [
            [c_n * np.exp(2j * np.pi * (nn - len(self.function_coefficients[f_i])//2) * np.linspace(0, 1, num=self.PRECISION))
             for nn, c_n in enumerate(self.function_coefficients[f_i])] for f_i in range(len(self.RADIO_NAMES))]

        self.update_canvas(pnts=True, cffc=True)

    def points_of(self, f_id: str):
        xs = np.linspace(0, 1, num=self.PRECISION)
        if f_id == 'sin': return np.sin(np.pi * 2 * xs)
        if f_id == 'rect': return np.where(xs < 0.5, -1, 1)
        if f_id == 'lin': return xs*(2+2j)-1-1j
        if f_id == 'square': return np.array([(1 + 1j - 8j * x if x < 0.25 else (1 - 1j - 8 * (x - 0.25) if x < 0.5 else (-1 - 1j + 8j * (x - 0.5) if x < 0.75 else -1 + 1j + 8 * (x - 0.75)))) for x in xs])
        if f_id == 'unknown': return fourier_math.get_svg_points('kolleg_logo.svg', self.PRECISION, self.KOLLEG_SIZE)

    def on_radio(self): self.update_canvas(pnts=True, cffc=True)

    def set_time(self, t: float): self.slider_values[self.SLIDER_NAMES.index('Zeit t')].set(t)
    def get_time(self): return self.slider_values[self.SLIDER_NAMES.index('Zeit t')].get()

    def do_animation(self):
        speed_f = self.slider_values[self.SLIDER_NAMES.index('Geschwindigkeit')].get()
        self.set_time((self.get_time() + self.SPEED[0] * speed_f) % 1)
        self.update_canvas(cffc=True)
        if self.animation_event.is_set(): self.after(int(self.SPEED[1]*1000), self.do_animation)

    def on_animation(self):
        if self.is_animation.get():
            self.animation_event.set()
            self.do_animation()
        else: self.animation_event.clear()

    def update_canvas(self, **kwargs):
        function_i = self.RADIO_NAMES.index(self.selected_radio.get())
        approx_n = int(self.slider_values[self.SLIDER_NAMES.index('Approximation N')].get())
        if kwargs.get('pnts', False):
            to = int(self.slider_values[self.SLIDER_NAMES.index('Parameter')].get() * len(self.function_points[function_i]))
            self.canvas.update_points(self.function_points[function_i][:to])

        if kwargs.get('cffc', False):
            pointers = self.fourier_parts[function_i][self.MAX_N-approx_n:self.MAX_N+approx_n+1]
            self.canvas.update_pointers(pointers, self.get_time())

    def slider_changed(self, var, _1, _2):
        ind = int(var[-1])
        if self.SLIDER_NAMES[ind] == 'Parameter': self.update_canvas(pnts=True)
        if self.SLIDER_NAMES[ind] == 'Approximation N': self.update_canvas(cffc=True)
        if self.SLIDER_NAMES[ind] == 'Zeit t': self.update_canvas(cffc=True)



FourierController().mainloop()

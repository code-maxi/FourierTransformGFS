import tkinter as tk
import fourier_canvas

class FourierController(tk.Tk):
    SLIDER_NAMES = ['Zeit', 'Geschwindigkeit']
    SLIDER_RANGE = [(0,1), (0,1)]
    SIZE = 1200
    PRESICION = 0.01

    def __init__(self):
        super().__init__()
        self.title('Komplexe Fourierreihe')
        self.canvas = fourier_canvas.FourierCanvas(self, self.SIZE, self.PRECISION)
        self.slider_values = [tk.DoubleVar() for _ in self.SLIDER_NAMES]
        self.slider_labels = [tk.Label(self, text=n) for n in self.SLIDER_NAMES ]

        self.sliders = [tk.Scale(
            self, length=int(self.SIZE * 0.65),
            resolution=0.01, from_=self.SLIDER_RANGE[i][0],
            to=self.SLIDER_RANGE[i][1], orient='horizontal',
            variable=self.slider_values[i],
            command=lambda _: self.slider_changed(i)
        ) for i in range(len(self.SLIDER_NAMES))]

        for i in range(len(self.SLIDER_NAMES)):
            self.sliders[i].grid(column=1, row=i+1)
            self.slider_labels[i].grid(column=0, row=i+1)

    def slider_changed(self, n: str):
        print(f'Slider {n} value {self.slider_values[self.SLIDER_NAMES.index(n)].get()}')

FourierController().mainloop()

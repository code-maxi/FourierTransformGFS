import threading
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

max_approx = 30
xs = np.arange(0, 1, 0.002)

ys_fs = {'f': np.zeros_like(xs), 's': np.zeros_like(xs)}
fourier_parts = {'a': 0.0, 'p': np.zeros([2, max_approx, len(xs)])}

main_fig, main_ax = plt.subplots()
main_ax.set_ylim([-1.5, 1.5])
main_ax.set_title('Vergleich einer beliebigen Funktion $f(t)$ mit deren Fourier-Approximation $s_n(t)$')
plt.subplots_adjust(bottom=0.35)

slider_axes = plt.axes((0.3, 0.1, 0.6, 0.04))
slider = Slider(slider_axes, 'Approximierungsgrad n ', 1, max_approx, valstep=1)
f_line = main_ax.plot(xs, ys_fs['f'], linestyle='dashed', label='$f(x)$')[0]
s_line = main_ax.plot(xs, np.zeros_like(xs), c='r', label='$s_n(t)$')[0]

main_ax.grid()
main_ax.legend()

fourier_fig, fourier_ax = plt.subplots()
fourier_ax.set_ylim([0, 1])
fourier_ax.set_title('Zusammensetzung der Fourier-Approximation $s_n(t)$')

ys_freq = [0.8*10**(-n/max_approx) for n in range(max_approx+1)]
ys_freq_labels = ['$s_n(t)$'] + [f'${max_approx-n} / T$' for n in range(max_approx)]
fourier_ax.set_yticks(ys_freq, ys_freq_labels)

fourier_ax.axhline(y=ys_freq[0], c='gray', linestyle='dashed')
lines = [[fourier_ax.plot(xs, np.zeros_like(xs) + ys_freq[n+1])[0] for n in range(max_approx)] for c in ['r', 'b']]

def integral(ys, fac) -> float:
    return sum([(y * fac(i/len(ys)))/len(ys) for i, y in enumerate(ys)])

def update_fourier(_=0.0):
    fourier_parts['a'] = integral(ys_fs['f'], lambda _: 1)
    for n in range(1, max_approx+1):
        if n <= slider.val:
            a_n = 2 * integral(ys_fs['f'], lambda x: np.cos(2 * np.pi * n * x))
            b_n = 2 * integral(ys_fs['f'], lambda x: np.sin(2 * np.pi * n * x))
            fourier_parts['p'][0][n-1] = a_n * np.cos(2 * np.pi * n * xs)
            fourier_parts['p'][1][n-1] = b_n * np.sin(2 * np.pi * n * xs)
        else:
            fourier_parts['p'][0][n-1] *= 0
            fourier_parts['p'][1][n-1] *= 0
    ys_fs['s'] = fourier_parts['a'] + sum(sum(fourier_parts['p']))

    f_line.set_ydata(ys_fs['f'])
    s_line.set_ydata(ys_fs['s'])

    for fig in [main_fig, fourier_fig]:
        fig.canvas.draw()
        fig.canvas.flush_events()

is_dragging = threading.Event()

def mouse_press(_): is_dragging.set()

def mouse_release(_):
    is_dragging.clear()
    update_fourier()

def mouse_move(evt):
    try:
        if is_dragging.is_set() and 0 <= evt.xdata <= 1 and -1.5 <= evt.ydata <= 1.5:
            for d in range(30):
                i = int(evt.xdata*len(xs)+0.5)+d
                if i < len(ys_fs['f']): ys_fs['f'][i] = max(min(evt.ydata, 1), -1)

            f_line.set_ydata(ys_fs['f'])
            main_fig.canvas.draw()
            main_fig.canvas.flush_events()
    except TypeError: print('error, no matter')

main_fig.canvas.mpl_connect('button_press_event', mouse_press)
main_fig.canvas.mpl_connect('button_release_event', mouse_release)
main_fig.canvas.mpl_connect('motion_notify_event', mouse_move)
slider.on_changed(update_fourier)

update_fourier()

plt.show()
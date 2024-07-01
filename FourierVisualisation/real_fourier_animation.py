import sys
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
tp = bool(int(sys.argv[1]))
xs = np.arange(0, np.pi*4, 0.01)
max_approx = 28

def func(x):
    return (1 if 0 <= x % (2*np.pi) < np.pi else -1) if tp else (x + np.pi) % (2*np.pi) - np.pi

def s_n(n: int, x):
    return (0 if n % 2 == 0 else np.sin(n*x)) if tp else 2*((-1)**(n+1))/n * np.sin(n*x)

def ampitude(n: int):
    return 1 if tp else 2/n

approx_sins = np.array([[s_n(max_approx-n, x) for x in xs] for n in range(max_approx)])
max_val = approx_sins.max()
amplitudes = [ampitude(max_approx-n)*2 for n in range(max_approx)]

fig1, ax1 = plt.subplots()
ax1.set_title('Vergleich der Funktion $f(t)$ mit deren Fourier-Approximation $s_n(t)$')
plt.subplots_adjust(bottom=0.35)
slax = plt.axes((0.3, 0.1, 0.6, 0.04))
slider = Slider(slax, 'Approximierungsgrad n ', 1, max_approx, valstep=1)
ax1.plot(xs, [func(x) for x in xs], linestyle='dashed', label='$f(x)$')
resline = ax1.plot(xs, np.zeros_like(xs), c='r', label='$s_n(t)$')[0]
ax1.grid()
ax1.legend()

fig2, ax2 = plt.subplots()
ax2.set_title('Zusammensetzung der Fourier-Approximation $s_n(t)$')
ax2.set_ylim([-amplitudes[0], sum(amplitudes) + sum(approx_sins).max()])
ax2.set_yticks([
    sum(amplitudes[:n]) for n in range(max_approx + 1)],
    ['$s_n(t)$' if n == max_approx else f'${max_approx-n} / T$' for n in range(max_approx+1)]
)
ax2.axhline(y=sum(amplitudes), c='gray', linestyle='dashed')
lines = [ax2.plot(xs, np.zeros_like(xs) - 1)[0] for n in range(max_approx+1)]

def update(val):
    for n in range(max_approx):
        ydat = sum(amplitudes[:n]) + approx_sins[n] * (1 if max_approx - n <= val else 0) / max_val
        lines[n].set_ydata(ydat)
    ysum = sum(approx_sins[-val:]) / max_val
    lines[max_approx].set_ydata(ysum + sum(amplitudes))
    resline.set_ydata(ysum)
    for fig in [fig1, fig2]:
        fig.canvas.draw()
        fig.canvas.flush_events()

slider.on_changed(update)

plt.show()

import numpy as np
import matplotlib.pyplot as plt
tones = 440, 550, 660
names = 'a', 'cis', 'e'
precision = 128
interval = 0, 10, 0.01
ts = np.arange(interval[0], interval[1], interval[2])

plt.rcParams.update({'font.size': 20})
plt.figure().set_figwidth(20)

am, ap = -1, 1
if True:
    ys = [sum([np.sin(2*np.pi*f*t/1000) for f in tones]) for t in ts]
    plt.plot(ts, ys, c='r', linewidth=3)
    am, ap = min(ys), max(ys)
else:
    for i, f in enumerate(tones[:1]):
        ys = [np.sin(2*np.pi*f*t/1000) for t in ts]
        plt.plot(ts, ys, linewidth=3, label=names[i]+'$(t) = sin(2\\pi \\cdot '+str(f)+' Hz \\cdot t)$')
    plt.legend()

plt.axhline(y=0, c='black')
plt.gca().set_ylabel('Amplitude')
plt.gca().set_xlabel('Zeit $t$ (in ms)')
plt.gca().set_yticks([am, 0, ap], ['$-\\hat{s}$', '0', '$\\hat{s}$'])
plt.grid()
plt.show()

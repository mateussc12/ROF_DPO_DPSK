import matplotlib.pyplot as plt
import numpy as np
from funcs import AWGN_noise
import os

t = np.arange(0, 60, 0.1)
x = np.sin(t)
SNR = 15


y = AWGN_noise.AWGN_noise(x, SNR, NPPS=1)
plt.plot(t, x, label='Original Signal')
plt.plot(t, y, label='Signal with AWGN')
plt.title('python')
plt.legend()

current_dir = os.getcwd()

t = np.genfromtxt(os.path.join(current_dir, 't.csv'), delimiter=',')
x = np.genfromtxt(os.path.join(current_dir, 'x.csv'), delimiter=',')
y = np.genfromtxt(os.path.join(current_dir, 'y.csv'), delimiter=',')

plt.figure()
plt.plot(t, x, label='Original Signal')
plt.plot(t, y, label='Signal with AWGN')
plt.title('matlab')
plt.legend()

plt.show()

import numpy as np
from scipy.special import erfc
from scipy.integrate import dblquad
from decimal import *
getcontext().prec = 4

# N_ring_series = np.array([2, 3, 5])
N_ring = 5
R = 1  # m
pitch = 0.2  # m
alpha = 1e-6  # m2/s
t_series = np.arange(10000, 3e7 + 1, 1e6)
t_1 = int(1e6)
h = 2  # m

# gs_series = []
# for N_ring in N_ring_series:
gs_series = []
for t in t_series:
    gs = Decimal(0)
    for i in range(1, N_ring + 1):
        for j in range(1, N_ring + 1):
            if i != j:
                def d(w, phi):
                    return np.sqrt((pitch * (i - j) + R * (np.cos(phi) - np.cos(w)))**2 +
                               (R * (np.sin(phi) - np.sin(w)))**2)

                def fun(w, phi):
                    return erfc(d(w, phi) / (2 * np.sqrt(alpha * t))) / d(w, phi) - erfc(np.sqrt(d(w, phi)**2 + 4 * h**2) / (2 * np.sqrt(alpha * t))) / np.sqrt(d(w, phi)**2 + 4 * h**2)

                b, _ = dblquad(fun, 0, 2 * np.pi, lambda phi: 0, lambda phi: 2 * np.pi, epsabs=1e-2, epsrel=1e-2)
                print(b)
                gs += Decimal(b)

    print(f"gs: {gs}")
    gs_series.append(gs)

# plt.plot(t_series, gs_series)
# plt.show()
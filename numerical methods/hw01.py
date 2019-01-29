import math
import cmath
import numpy as np
from matplotlib import pyplot as plt


# Function from task 2.
def w_a(z):
    N = 1000001
    ans = 0

    for k in range(1, N + 1):
        ans += 1 / (k ** 2 - k - z)

    return ans


# Function from task 2.
def w_b(z):
    # N = 333335
    N = 1415
    ans = math.pi ** 2 / 6

    for k in range(1, N + 1):
        ans += (k + z) / ((k ** 2 - k - z) * (k ** 2))

    return ans


# Function from task 3.
def s(z, N):
    s1 = z
    s2 = s1 + z ** 2 / 3
    s3 = s2 + z ** 3 / 5
    ans = s3 - (s3 - s2) ** 2 / ((s3 - s2) - (s2 - s1))

    for k in range(4, N):
        s1 = s2
        s2 = s3
        s3 += z ** k / (2 * k - 1)

        if (s3 - s2) - (s2 - s1) != 0:
            ans = s3 - (s3 - s2) ** 2 / ((s3 - s2) - (s2 - s1))

    return ans


# Plot function for values in given range with given step.
def plot(f, a, b, step, abs_value=None):
    x = np.arange(a + step, b, step)
    y = [f(xi) for xi in x]

    fig, ax = plt.subplots()
    ax.plot(x, y, color='blue')
    ax.plot(x, y, 'o', color='blue')

    if abs_value is not None:
        ax.axhline(y=-abs_value, color='blue', linestyle='dashed')
        ax.axhline(y=abs_value, color='blue', linestyle='dashed')

    plt.plot()
    plt.show()


# Plot function with approximation line.
def plot_approximation(f, a, b, step):
    x = np.arange(a + step, b, step)
    y = [f(xi) for xi in x]

    fig, ax = plt.subplots()
    ax.plot(x, y, color='blue')
    ax.plot(x, y, 'o', color='blue')

    approximation = np.polyfit(x, y, 1)
    xa = np.array([0, 9])
    ya = [approximation[0] * xi + approximation[1] for xi in xa]

    ax.plot(xa, ya,
            linestyle='dashed',
            label='y = %f * x + %f' % (approximation[0], approximation[1]))

    plt.legend()
    plt.plot()
    plt.show()


def plot_eitken_error(z):
    s0 = s(z, 1000000)
    log_error = lambda logN: math.log2(np.linalg.norm(s(z, 2 ** logN) - s0))
    plot_approximation(log_error, 1, 9, 1)


if __name__ == '__main__':
    # task 2
    a = 0
    b = 2
    step = 5e-2

    plot(w_a, a, b, step)
    plot(w_b, a, b, step)
    plot(lambda z: w_a(z) - w_b(z), a, b, step, abs_value=2e-6)

    # task 3
    plot_eitken_error(-0.9)
    plot_eitken_error(-1)
    plot_eitken_error(cmath.exp(complex(0, 1) * 3 * math.pi / 4))
    plot_eitken_error(complex(0, 1))

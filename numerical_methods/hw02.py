import math
import numpy as np
from matplotlib import pyplot as plt


def lagrange(f, a, b, N):
    xk = a + np.arange(0, N + 1) * (b - a) / N
    yk = [f(xi) for xi in xk]

    def p(x):
        ans = 0
        for k in range(N + 1):
            prod = yk[k]
            for i in range(N + 1):
                if i != k:
                    prod *= (x - xk[i]) / (xk[k] - xk[i])
            ans += prod
        return ans

    return p


def lagrange_cheb(f, a, b, N):
    t = np.array([math.cos(math.pi / 2 * (2 * k - 1) / (N + 1))
                  for k in np.arange(1, N + 2)])
    xk = 0.5 * (a + b) + 0.5 * (b - a) * t
    yk = [f(xi) for xi in xk]

    def p(x):
        ans = 0
        for k in range(N + 1):
            prod = yk[k]
            for i in range(N + 1):
                if i != k:
                    prod *= (x - xk[i]) / (xk[k] - xk[i])
            ans += prod
        return ans

    return p


# Plot functions for values in given range with given step.
def plot(fs, a, b, step, abs_value=None):
    x = np.arange(a + step, b, step)
    fig, ax = plt.subplots()

    for f in fs:
        y = [f(xi) for xi in x]
        ax.plot(x, y)

    if abs_value is not None:
        ax.axhline(y=-abs_value, color='blue', linestyle='dashed')
        ax.axhline(y=abs_value, color='blue', linestyle='dashed')

    plt.plot()
    plt.show()


def max_value(f, a, b, step):
    x = np.arange(a + step, b, step)
    y = [f(xi) for xi in x]
    return max(y)


def average_value(f, a, b, step):
    x = np.arange(a + step, b, step)
    y = [f(xi) for xi in x]
    return sum(y) / len(y)


def error(p, f):
    return lambda x: math.fabs(p(x) - f(x))


if __name__ == '__main__':
    # task 1
    f = lambda x: x * math.sin(2 * x)
    x0 = 100

    # task 1.A
    p = lagrange(f, x0 - 5, x0 + 5, 5)
    plot([error(p, f)], x0 - 5, x0 + 5, 1e-3)
    print(max_value(error(p, f), x0 - 5, x0 + 5, 1e-3))

    p = lagrange(f, x0 - 5, x0 + 5, 10)
    plot([error(p, f)], x0 - 5, x0 + 5, 1e-3)
    print(max_value(error(p, f), x0 - 5, x0 + 5, 1e-3))

    p = lagrange(f, x0 - 5, x0 + 5, 15)
    plot([error(p, f)], x0 - 5, x0 + 5, 1e-3)
    print(max_value(error(p, f), x0 - 5, x0 + 5, 1e-3))

    # task 1.B
    plot([lambda N: max_value(error(lagrange(f, x0 - 5, x0 + 5, N), f),
                              x0 - 5,
                              x0 + 5,
                              1e-2)], 4, 51, 1)

    plot([lambda N: average_value(error(lagrange(f, x0 - 5, x0 + 5, N), f),
                                  x0 - 5,
                                  x0 + 5,
                                  1e-2)], 4, 51, 1)

    # task 1.C
    plot([lambda N: max_value(error(lagrange_cheb(f, x0 - 5, x0 + 5, N), f),
                              x0 - 5,
                              x0 + 5,
                              1e-2)], 4, 51, 1)

    plot([lambda N: average_value(error(lagrange_cheb(f, x0 - 5, x0 + 5, N), f),
                                  x0 - 5,
                                  x0 + 5,
                                  1e-2)], 4, 51, 1)

    # Comparing
    plot([lambda N: max_value(error(lagrange(f, x0 - 5, x0 + 5, N), f),
                              x0 - 5,
                              x0 + 5,
                              1e-2),
          lambda N: max_value(error(lagrange_cheb(f, x0 - 5, x0 + 5, N), f),
                              x0 - 5,
                              x0 + 5,
                              1e-2)], 4, 51, 1)


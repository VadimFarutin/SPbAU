import numpy as np
from matplotlib import pyplot as plt


############# Task 10 #############

# Euler method
def euler(f, x0, u0, T, N, a):
    x_cur = x0
    y_cur = u0
    x = [x_cur]
    y = [y_cur[0]]
    h = T / N

    for i in range(N):
        y_cur += h * f(a, x_cur, y_cur)
        x_cur += h
        x.append(x_cur)
        y.append(y_cur[0])

    return x, np.array(y)


# Runge-Knuth method
def runge_knuth(f, x0, u0, T, N, a, beta=0.5):
    x_cur = x0
    y_cur = u0
    x = [x_cur]
    y = [y_cur[0]]
    h = T / N
    h2b = h / (2 * beta)

    for i in range(N):
        y_cur += h * ((1 - beta) * f(a, x, y_cur)
                      + beta * f(a, x + h2b, y_cur + h2b * f(a, x, y_cur)))
        x_cur += h
        x.append(x_cur)
        y.append(y_cur[0])

    return x, np.array(y)


def plot_euler_solution(f, x0, u0, N, T, a):
    for n in N:
        x, y = euler(f, x0(a), u0(a), T, n, a)
        plt.plot(x, np.log10(y), label='N = %d' % n)

    plt.xlabel("x")
    plt.ylabel("log(y)")
    plt.legend()
    plt.show()


def plot_error(methods, u, f, x0, u0, N, T, a):
    x = np.arange(1, N + 1, 1)

    for method in methods:
        y = []

        for n in x:
            xi, yi = method(f, x0(a), u0(a), T, n, a)
            ui = np.array([u(a, t) for t in xi])
            y.append(max(np.abs(yi - ui)))

        plt.plot(x, np.log10(y), label='%s' % method.__name__)

    plt.axhline(y=np.log10(1e-3))
    plt.xlabel("N")
    plt.ylabel("log(error)")
    plt.legend()
    plt.show()


# Solution
u = lambda a, x: np.e ** (-a * x)

f = lambda a, x, y: np.array([y[1], a ** 2 * y[0]])
x0 = lambda a: 0.0
u0 = lambda a: np.array([1.0, -a])
N = [10, 50, 100]
N_max = 500
T = 10
a = [1.0, np.sqrt(20)]
methods = [euler, runge_knuth]

for ai in a:
    plot_euler_solution(f, x0, u0, N, T, ai)
    plot_error(methods, u, f, x0, u0, N_max, T, ai)

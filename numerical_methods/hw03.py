import math
import numpy as np
from matplotlib import pyplot as plt


############# Task 1 #############

def df_approximate(f, x0, alpha, h):
    y0 = f(x0 - h / alpha)
    y1 = f(x0)
    y2 = f(x0 + h * alpha)

    return ((y1 - y0) * (alpha - 1 / alpha) + (y2 - y0) / (alpha ** 3 + alpha)) / h


def plot_error(f, df, x0, alpha, h_a, h_b, h_step):
    df_real = df(x0)

    for a in alpha:
        x = np.arange(h_a, h_b + h_step, h_step)
        y = np.array([abs(df_approximate(f, x0, a, xi) - df_real) for xi in x])
        plt.plot(x, y, label='alpha %f' % a)

    plt.legend()
    plt.show()


def plot_log_error(f, df, x0, alpha, h_a, h_b, h_step):
    df_real = df(x0)

    for a in alpha:
        x = np.arange(h_a, h_b + h_step, h_step)
        y = np.array([np.log2(abs(df_approximate(f, x0, a, xi) - df_real)) for xi in x])
        plt.plot(x, y, label='alpha %f' % a)

    plt.legend()
    plt.show()


f = lambda x: np.sin(x)
df = lambda x: np.cos(x)
x0 = 10

alpha = np.arange(1, 2 + 0.25, 0.25)
plot_error(f, df, x0, alpha, 1e-8, 1 + 1e-2, 1e-2)
plot_log_error(f, df, x0, alpha, 0.1, 0.2, 1e-2)


############# Task 2.A #############

def I_trapezium(f, a, b, n):
    step = (b - a) / n
    ai = a
    res = f(ai) / 2
    ai += step

    for i in range(1, n):
        res += f(ai)
        ai += step

    res += f(ai) / 2
    res *= step

    return res


def I_Simpson(f, a, b, n):
    step = (b - a) / n
    ai = a
    res = f(ai) + 4 * f(ai + step / 2)
    ai += step

    for i in range(1, n):
        res += 2 * f(ai) + 4 * f(ai + step / 2)
        ai += step

    res += f(ai)
    res *= step / 6

    return res


def plot_I_error(f, I, I_func, a, b, n_a, n_b, n_step):
    for func in I_func:
        x = np.arange(n_a, n_b + n_step, n_step)
        y = np.array([abs(func(f, a, b, xi) - I) for xi in x])
        plt.plot(x, y, label='%s' % func)

    plt.legend()
    plt.show()


def plot_I_log_error(f, I, I_func, a, b, n_a, n_b, n_step):
    for func in I_func:
        x = np.arange(n_a, n_b + n_step, n_step)
        y = np.array([np.log2(abs(func(f, a, b, xi) - I)) for xi in x])
        plt.plot(x, y, label='%s' % func)

    plt.legend()
    plt.show()


f = lambda x: 1 / (1 + 9 * x ** 2)
a = -1
b = 5
I = (np.arctan(3 * b) - np.arctan(3 * a)) / 3

I_func = [I_trapezium, I_Simpson]
plot_I_error(f, I, I_func, a, b, 1, 1000, 1)
plot_I_log_error(f, I, I_func, a, b, 1, 1000, 1)


############# Task 2.B #############

def step_Runge(f, a, b, eps):
    H1 = 1e-3
    H2 = H1 / 2
    S_H1 = I_trapezium(f, a, b, int((b - a) / H1))
    S_H2 = I_trapezium(f, a, b, int((b - a) / H2))
    C = (S_H2 - S_H1) / (3 * H2 ** 2)

    return np.sqrt(eps / abs(C))


def step_fact(f, a, b, eps, I):
    MAX_N = 1000
    n = np.arange(1, MAX_N, 1)
    H = np.array([(b - a) / ni for ni in n])

    for i in range(MAX_N):
        error = abs(I_trapezium(f, a, b, n[i]) - I)
        if error < eps:
            return H[i]

    return H[MAX_N - 1]


print(step_Runge(f, a, b, 1e-6))
print(step_fact(f, a, b, 1e-6, I))
print(abs(step_Runge(f, a, b, 1e-6) - step_fact(f, a, b, 1e-6, I)))


############# Task 2.C #############

def newton_kotes_weights(a, b, N, n):
    def f_i(i):
        def f(q):
            res = 1
            for k in range(1, N + 1):
                if k != i:
                    res *= q - (k - 1)
            return res
        return f

    h = (b - a) / (N - 1)

    def lambda_i(i):
        return (-1) ** (N - i) * h \
               / np.math.factorial(i - 1) \
               / np.math.factorial(N - i) \
               * I_Simpson(f_i(i), 0, N - 1, n)

    return np.array([lambda_i(i) for i in range(1, N + 1)])


def plot_newton(N, a, b, n):
    x = range(2, N + 1)
    y = [min(newton_kotes_weights(a, b, i, n)) for i in x]

    plt.plot(x, y)
    plt.axhline(0, linestyle='dashed')
    plt.show()


a = -1
b = 1
n = 1000
N = 17

plot_newton(N, a, b, n)

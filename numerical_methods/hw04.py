import numpy as np
import scipy.special
from matplotlib import pyplot as plt


############# Task 1 #############

# Ищет корень на отрезке [a, b] методом секущих
def find_root(f, a, b):
    N = 10
    # x0, x1 -- две точки внутри отрезка
    x0 = a / 3 + b * 2 / 3
    x1 = a * 2 / 3 + b / 3

    for i in range(N):
        t = x1
        f1 = f(x1)

        if abs(f1 - f(x0)) < 1e-9:
            break

        x1 = t - f1 * (t - x0) / (f1 - f(x0))
        x0 = t

    return x1


# Ищет все корни для всех многочленов Лежандра <= n
def legendre_roots(n):
    roots = [[-1, 1]]

    for i in range(1, n + 1):
        roots_i = []
        f = scipy.special.legendre(i)
        roots_i.append(-1)

        for j in range(i):
            a = roots[i - 1][j]
            b = roots[i - 1][j + 1]
            x = find_root(f, a, b)
            roots_i.append(x)

        roots_i.append(1)
        roots.append(roots_i)

    ans = [roots_i[1:-1] for roots_i in roots]
    return ans[1:]


ROOTS = []


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


# Ищет веса для многочлена Лежандра степени n
def legendre_weights(n):
    roots = ROOTS[n - 1]

    def f_j(j):
        def f(q):
            res = 1
            for k in range(n):
                if k != j:
                    res *= (q - roots[k]) / (roots[j] - roots[k])
            return res

        return f

    weights = []

    for j in range(n):
        w = I_Simpson(f_j(j), -1, 1, 200)
        weights.append(w)

    return weights


# Считает интеграл через квадратурную формулу
def I_Gauss(f, a, b, n):
    weights = legendre_weights(n)
    roots = ROOTS[n - 1]
    roots_adj = [(a + b) / 2 + x * (b - a) / 2 for x in roots]

    ans = (b - a) / 2 * sum([wi * f(xi) for wi, xi in zip(weights, roots_adj)])
    return ans


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
        y = np.array([np.log10(abs(func(f, a, b, xi) - I)) for xi in x])
        plt.plot(x, y, label='%s' % func)

    plt.xlabel("n")
    plt.ylabel("log_10(error)")
    plt.legend()
    plt.show()


def plot_I_log_error_log_x(f, I, I_func, a, b, n_a, n_b, n_step):
    for func in I_func:
        x = np.arange(n_a, n_b + n_step, n_step)
        y = np.array([np.log10(abs(func(f, a, b, xi) - I)) for xi in x])
        plt.plot(np.log10(x), y, label='%s' % func)

    plt.xlabel("log_10(n)")
    plt.ylabel("log_10(error)")
    plt.legend()
    plt.show()


f = lambda x: 1 / (1 + 9 * x ** 2)
a = -1
b = 5
I = (np.arctan(3 * b) - np.arctan(3 * a)) / 3
n_a = 1
n_b = 80

ROOTS = legendre_roots(n_b)
I_func = [I_Gauss, I_Simpson]
plot_I_log_error(f, I, I_func, a, b, n_a, n_b, 1)

import numpy as np
import time
from matplotlib import pyplot as plt


############# Task 7.1 #############

# analytic solution
def u(x):
    return (np.exp(x) - np.exp(-x)) / (np.exp(-1) - np.exp(1)) + x


def A(N):
    h = 1.0 / (N + 1)
    h2 = h ** 2
    res = np.zeros((N, N))

    for i in range(N):
        res[i][i] = 2 / h2 + 1

    for i in range(N - 1):
        res[i][i + 1] = - 1 / h2
        res[i + 1][i] = - 1 / h2

    return res


def b(N):
    h = 1.0 / (N + 1)
    return np.array([h * i for i in range(1, N + 1)])


def get_real(N):
    h = 1.0 / (N + 1)
    x = h * np.arange(1, N + 1)
    return np.array([u(xi) for xi in x])


def get_standard(N):
    return np.linalg.solve(A(N), b(N))


############# Task 7.2 #############

def get_running(N):
    h = 1.0 / (N + 1)
    h2 = h ** 2
    d_value = 2 / h2 + 1
    subd_value = 1 / h2
    s = b(N)

    alpha = [subd_value / d_value]
    beta = [s[0] / d_value]

    for i in range(1, N):
        alpha.append(subd_value / (d_value - alpha[-1] * subd_value))
        beta.append((s[i] + beta[-1] * subd_value) / (d_value - alpha[-1] * subd_value))

    alpha.reverse()
    beta.reverse()
    ans = [beta[0]]
    for i in range(1, N):
        ans.append(ans[-1] * alpha[i] + beta[i])
    ans.reverse()

    return np.array(ans)


############# Task 7 plots #############

def error_xy(func, n_a, n_b, n_step):
    x = np.arange(n_a, n_b + n_step, n_step)
    y = np.array([max(abs(get_real(xi) - func(xi))) for xi in x])
    return x, y


def plot_error(funcs, n_a, n_b, n_step):
    for func in funcs:
        x, y = error_xy(func, n_a, n_b, n_step)
        plt.plot(x, y, label='%s' % func)

    plt.xlabel("N")
    plt.ylabel("max error")
    plt.legend()
    plt.show()


def plot_log_error(funcs, n_a, n_b, n_step):
    for func in funcs:
        x, y = error_xy(func, n_a, n_b, n_step)
        plt.plot(x, np.log10(y), label='%s' % func)

    plt.xlabel("N")
    plt.ylabel("log10(max error)")
    plt.legend()
    plt.show()


def plot_log_error_log_x(funcs, n_a, n_b, n_step):
    for func in funcs:
        x, y = error_xy(func, n_a, n_b, n_step)
        plt.plot(np.log10(x), np.log10(y), label='%s' % func)

    plt.xlabel("log10(N)")
    plt.ylabel("log10(max error)")
    plt.legend()
    plt.show()


def measure_time(func, N):
    start = time.clock()
    func(N)
    end = time.clock()
    return end - start


def time_xy(func, n_a, n_b, n_step):
    x = np.arange(n_a, n_b + n_step, n_step)
    y = np.array([measure_time(func, xi) for xi in x])
    return x, y


def plot_time(funcs, n_a, n_b, n_step):
    for func in funcs:
        x, y = time_xy(func, n_a, n_b, n_step)
        plt.plot(x, y, label='%s' % func)

    plt.xlabel("N")
    plt.ylabel("clocks")
    plt.legend()
    plt.show()


def plot_log_time_log_x(funcs, n_a, n_b, n_step):
    for func in funcs:
        x, y = time_xy(func, n_a, n_b, n_step)
        plt.plot(np.log10(x), np.log10(y), label='%s' % func)

    plt.xlabel("log10(N)")
    plt.ylabel("log10(clocks)")
    plt.legend()
    plt.show()


############# Task 8 #############

def get_SOR(A, b, N, n, w):
    stages = []
    x = np.zeros(N)

    for _ in range(n):
        x_next = []

        for i in range(N):
            sum1 = sum([A[i][j] * x_next[j] for j in range(i)])
            sum2 = sum([A[i][j] * x[j] for j in range(i + 1, N)])
            x_next.append((1 - w) * x[i] + w * (b[i] - sum1 - sum2) / A[i][i])

        stages.append(np.array(x_next))
        x = np.copy(x_next)

    return stages


def plot_stages_error(N, w, n):
    real = get_running(N)

    for wi in w:
        stages = get_SOR(A(N), b(N), N, n, wi)
        x = np.arange(1, n + 1)
        y = [max(np.abs(real - stage)) for stage in stages]
        plt.plot(np.log10(x), np.log10(y), label='w=%s' % wi)

    plt.xlabel("log10(iteration number)")
    plt.ylabel("log10(error)")
    plt.title("N=%d" % N)
    plt.legend()
    plt.show()


funcs = [get_standard, get_running]
plot_log_error_log_x(funcs, 1, 1000, 1)
plot_log_time_log_x(funcs, 1, 2000, 10)

w = [1, 1.3, 1.6, 1.8, 1.9]
n = 1000

for N in [10, 15, 25, 40, 60, 90]:
    plot_stages_error(N, w, n)

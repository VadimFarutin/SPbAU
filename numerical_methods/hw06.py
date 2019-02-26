import numpy as np
from matplotlib import pyplot as plt


############# Task 9 #############

def hilbert_matrix(N):
    h = [[1 / (i + j - 1) for j in range(1, N + 1)] for i in range(1, N + 1)]
    return np.array(h)


def max_eigenvalue_iter(A, N, n):
    x_prev = np.ones(N)
    x_cur = np.dot(A, x_prev)
    lambda_cur = x_cur[0] / x_prev[0]

    for i in range(n):
        x_prev = x_cur
        x_cur = np.dot(A, x_prev)
        lambda_cur = x_cur[0] / x_prev[0]
        x_cur = x_cur / np.linalg.norm(x_cur)

    return lambda_cur


def min_eigenvalue_shift(A, N, n):
    alpha = max_eigenvalue_iter(A, N, n) + 1
    B = A - alpha * np.identity(N)
    lambda_min = max_eigenvalue_iter(B, N, n)

    return lambda_min + alpha


def condition_number(A, N, n):
    return max_eigenvalue_iter(A, N, n) / min_eigenvalue_shift(A, N, n)


def plot_f(f, n_a, n_b, n_step, n_iter):
    x = np.arange(n_a, n_b + n_step, n_step)
    y = np.array([f(hilbert_matrix(xi), xi, n_iter) for xi in x])
    plt.plot(x, np.log10(y))

    # y1 = np.array([(min(np.linalg.eig(hilbert_matrix(xi))[0])) for xi in x])
    # plt.plot(x, np.log10(y1))

    plt.xlabel("N")
    plt.ylabel("log(min_eig(A))")
    plt.legend()
    plt.show()


N = 5
n = 20000
A = hilbert_matrix(N)
# values, _ = np.linalg.eig(A)

plot_f(min_eigenvalue_shift, 1, N, 1, n)

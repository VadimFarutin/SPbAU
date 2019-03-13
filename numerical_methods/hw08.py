import numpy as np
from matplotlib import pyplot as plt


############# Task 11 #############

def net_app(l, R, N):
    h = R / N
    p = lambda x: l * (l + 1) / x ** 2 - 2 / x
    q = lambda x: 1
    A = np.zeros((N - 1, N - 1))

    for i in range(N - 1):
        if i != 0:
            A[i][i - 1] = 1 / h ** 2
        A[i][i] = - (2 / h ** 2 + p((i + 1) * h))
        if i != N - 2:
            A[i][i + 1] = 1 / h ** 2
        A[i] /= q((i + 1) * h)

    return np.linalg.eig(A)


def plot_solution(val, vec, R, N):
    h = R / N
    x = [i * h for i in range(N + 1)]
    y = np.array([0])
    y = np.append(y, vec)
    y = np.append(y, [0])

    plt.plot(x, y)
    plt.title(label='R: %f, lambda: %f' % (R, val))
    plt.xlabel("x")
    plt.ylabel("u(x)")
    plt.show()


l = 0
R = 10
N = 5000

values, vectors = net_app(l, R, N)
for i in range(5):
    plot_solution(values[i], vectors[i], R, N)

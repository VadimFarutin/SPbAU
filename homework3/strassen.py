import numpy as np


def zero_matrix(side_size, data_type):
    return np.zeros((side_size, side_size), dtype=data_type)


def empty_matrix(side_size, data_type):
    return np.empty((side_size, side_size), dtype=data_type)


def read_matrix(side_size):
    matrix = []
    for i in range(side_size):
        matrix.append(input().split())
    if str(float(matrix[0][0])) == matrix[0][0]:
        data_type = np.dtype(float)
    else:
        data_type = np.dtype(int)
    return np.matrix(matrix, dtype=data_type).reshape(side_size, side_size)


def print_matrix(matrix):
    for line in matrix:
        print(" ".join(map(str, line)))


def split_matrix(matrix):
    half_size = matrix.shape[0] // 2
    return [[np.matrix(matrix[:half_size, :half_size]), np.matrix(matrix[:half_size, half_size:])],
            [np.matrix(matrix[half_size:, :half_size]), np.matrix(matrix[half_size:, half_size:])]]


def multiply_matrices(matrix_res, matrix_a, matrix_b):
    side_size = matrix_a.shape[0]
    if side_size == 1:
        matrix_res[:, :] = np.dot(matrix_a, matrix_b)
    else:
        a = split_matrix(matrix_a)
        b = split_matrix(matrix_b)
        dtype = matrix_a.dtype
        half_size = side_size // 2
        I = empty_matrix(half_size, dtype)
        II = empty_matrix(half_size, dtype)
        III = empty_matrix(half_size, dtype)
        IV = empty_matrix(half_size, dtype)
        V = empty_matrix(half_size, dtype)
        VI = empty_matrix(half_size, dtype)
        VII = empty_matrix(half_size, dtype)
        multiply_matrices(I, a[0][0] + a[1][1], b[0][0] + b[1][1])
        multiply_matrices(II, a[1][0] + a[1][1], b[0][0])
        multiply_matrices(III, a[0][0], b[0][1] - b[1][1])
        multiply_matrices(IV, a[1][1], b[1][0] - b[0][0])
        multiply_matrices(V, a[0][0] + a[0][1], b[1][1])
        multiply_matrices(VI, a[1][0] - a[0][0], b[0][0] + b[0][1])
        multiply_matrices(VII, a[0][1] - a[1][1], b[1][0] + b[1][1])

        matrix_res[:half_size, :half_size] = I + IV - V + VII
        matrix_res[:half_size, half_size:] = III + V
        matrix_res[half_size:, :half_size] = II + IV
        matrix_res[half_size:, half_size:] = I + III - II + VI


def strassen(m_a, m_b):
    side_size = m_a.shape[0]
    increased_size = 2 ** (side_size.bit_length() - 1)
    if increased_size < side_size:
        increased_size *= 2

    dtype = m_a.dtype
    matrix_a = zero_matrix(increased_size, dtype)
    matrix_a[:side_size, :side_size] = m_a
    matrix_b = zero_matrix(increased_size, dtype)
    matrix_b[:side_size, :side_size] = m_b
    matrix_res = empty_matrix(increased_size, dtype)

    multiply_matrices(matrix_res, matrix_a, matrix_b)
    return matrix_res[:side_size, :side_size]


def main():
    n = int(input())
    matrix_a = read_matrix(n)
    matrix_b = read_matrix(n)
    print_matrix(strassen(matrix_a, matrix_b))


if __name__ == '__main__':
    main()

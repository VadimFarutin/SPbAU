import numpy as np


def zero_matrix(side_size):
    return np.zeros((side_size, side_size), dtype=np.int64)


def read_matrix(side_size):
    matrix = zero_matrix(side_size)
    for i in range(side_size):
        matrix[i] = input().split()
    return matrix


def print_matrix(matrix):
    for line in matrix.tolist():
        print(" ".join(map(str, line)))


def split_matrix(matrix):
    half_size = matrix.shape[0] // 2
    return [[np.matrix(matrix[:half_size, :half_size]), np.matrix(matrix[:half_size, half_size:])],
            [np.matrix(matrix[half_size:, :half_size]), np.matrix(matrix[half_size:, half_size:])]]


def multiply_matrices(matrix_res, matrix_a, matrix_b):
    side_size = matrix_a.shape[0]
    if side_size == 1:
        matrix_new = np.dot(matrix_a, matrix_b)
    else:
        a = split_matrix(matrix_a)
        b = split_matrix(matrix_b)
        half_size = side_size // 2
        I = zero_matrix(half_size)
        II = zero_matrix(half_size)
        III = zero_matrix(half_size)
        IV = zero_matrix(half_size)
        V = zero_matrix(half_size)
        VI = zero_matrix(half_size)
        VII = zero_matrix(half_size)
        multiply_matrices(I, a[0][0] + a[1][1], b[0][0] + b[1][1])
        multiply_matrices(II, a[1][0] + a[1][1], b[0][0])
        multiply_matrices(III, a[0][0], b[0][1] - b[1][1])
        multiply_matrices(IV, a[1][1], b[1][0] - b[0][0])
        multiply_matrices(V, a[0][0] + a[0][1], b[1][1])
        multiply_matrices(VI, a[1][0] - a[0][0], b[0][0] + b[0][1])
        multiply_matrices(VII, a[0][1] - a[1][1], b[1][0] + b[1][1])

        matrix_new = np.vstack((np.hstack((I + IV - V + VII, III + V)),
                                np.hstack((II + IV, I + III - II + VI))))

    for i in range(side_size):
        for j in range(side_size):
            matrix_res[i][j] = matrix_new[i][j]


def strassen(side_size):
    increased_size = 2 ** (side_size.bit_length() - 1)
    if increased_size < side_size:
        increased_size *= 2

    matrix_a = zero_matrix(increased_size)
    matrix_a[:side_size, :side_size] = read_matrix(side_size)
    matrix_b = zero_matrix(increased_size)
    matrix_b[:side_size, :side_size] = read_matrix(side_size)
    matrix_res = zero_matrix(increased_size)

    multiply_matrices(matrix_res, matrix_a, matrix_b)
    print_matrix(matrix_res[:side_size, :side_size])


def main():
    strassen(int(input()))


if __name__ == '__main__':
    main()

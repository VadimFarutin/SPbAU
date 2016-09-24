import numpy as np


def read_matrix(side_size):
    increased_size = 1
    while increased_size < side_size:
        increased_size *= 2

    matrix = np.zeros((increased_size, increased_size), dtype=np.int64)
    for i in range(side_size):
        line = input().split()
        for j in range(len(line)):
            matrix[i][j] = int(line[j])
    return matrix


def print_matrix(matrix, side_size):
    matrix = matrix[:side_size, :side_size].tolist()
    for line in matrix:
        print(" ".join(map(str, line)))


def split_matrix(matrix, side_size):
    half_size = side_size // 2
    return [[np.matrix(matrix[:half_size, :half_size]), np.matrix(matrix[:half_size, half_size:])],
            [np.matrix(matrix[half_size:, :half_size]), np.matrix(matrix[half_size:, half_size:])]]


def multiply_matrices(matrix_a, matrix_b, side_size):
    if side_size == 1:
        return np.dot(matrix_a, matrix_b)

    a = split_matrix(matrix_a, side_size)
    b = split_matrix(matrix_b, side_size)
    half_size = side_size // 2
    I = multiply_matrices(a[0][0] + a[1][1], b[0][0] + b[1][1], half_size)
    II = multiply_matrices(a[1][0] + a[1][1], b[0][0], half_size)
    III = multiply_matrices(a[0][0], b[0][1] - b[1][1], half_size)
    IV = multiply_matrices(a[1][1], b[1][0] - b[0][0], half_size)
    V = multiply_matrices(a[0][0] + a[0][1], b[1][1], half_size)
    VI = multiply_matrices(a[1][0] - a[0][0], b[0][0] + b[0][1], half_size)
    VII = multiply_matrices(a[0][1] - a[1][1], b[1][0] + b[1][1], half_size)

    return np.vstack((np.hstack((I + IV - V + VII, III + V)),
                      np.hstack((II + IV, I + III - II + VI))))


def main():
    n = int(input())
    matrix_a = read_matrix(n)
    matrix_b = read_matrix(n)
    print_matrix(multiply_matrices(matrix_a, matrix_b, matrix_a.shape[0]), n)


if __name__ == '__main__':
    main()

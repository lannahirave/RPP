import time

from generate_matrice_to_file import read_matrix_from_file


def multiply_matrices(matrix1, matrix2):
    result = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix2[0])):
            sum = 0
            for k in range(len(matrix2)):
                sum += matrix1[i][k] * matrix2[k][j]
            row.append(sum)
        result.append(row)
    return result


def save_matrix_to_file(matrix, filename):
    with open(filename, 'w') as file:
        for row in matrix:
            file.write(' '.join(map(str, row)) + '\n')


def main():
    matrix = read_matrix_from_file("matrix.txt")
    start_time = time.time()

    result = multiply_matrices(matrix, matrix)

    end_time = time.time()
    print("Time default:", end_time - start_time)
    save_matrix_to_file(result, "default_matrix.txt")


if __name__ == "__main__":
    main()

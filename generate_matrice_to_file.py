import random


def generate_random_matrix(N):
    matrix = []
    for _ in range(N):
        row = [random.randint(0, 9) for _ in range(N)]
        matrix.append(row)
    return matrix


def write_matrix_to_file(matrix, filename):
    with open(filename, 'w') as file:
        for row in matrix:
            file.write(' '.join(map(str, row)) + '\n')


def read_matrix_from_file(filename):
    matrix = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                row = list(map(int, line.strip().split()))
                matrix.append(row)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    return matrix


def main():
    try:
        N = int(input("Enter the size of the matrix (N): "))
        if N <= 0:
            print("Please enter a positive integer for N.")
            return

        matrix = generate_random_matrix(N)
        print("Randomly generated matrix:")
        for row in matrix:
            print(row)

        filename = "matrix.txt"
        write_matrix_to_file(matrix, filename)
        print(f"Matrix of size {N}x{N} has been written to {filename}.")

    except ValueError:
        print("Please enter a valid integer for N.")


if __name__ == "__main__":
    main()

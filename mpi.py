
from mpi4py import MPI
from time import time
from generate_matrice_to_file import read_matrix_from_file


def save_matrix_to_file(matrix, filename):
    with open(filename, 'w') as file:
        for row in matrix:
            file.write(' '.join(map(str, row)) + '\n')


def multiply_matrices(matrix1, matrix2):
    result = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix2[0])):
            row.append(sum(matrix1[i][k] * matrix2[k][j] for k in range(len(matrix1[0]))))
        result.append(row)
    return result


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    matrix2 = None
    rowsNum = 0
    chunks = []

    if rank == 0:
        matrix = read_matrix_from_file("matrix.txt")
        time_start = time()
        matrix1 = matrix.copy()
        rowsNum = len(matrix1)
        matrix2 = matrix.copy()

        chunkSize = rowsNum // size
        for i in range(size-1):
            chunk = []
            for ii in range(chunkSize):
                chunk.append(matrix1[ii + i * chunkSize])
            chunks.append(chunk)
        chunks.append(matrix1[chunkSize * (size-1):])
        

    matrix2 = comm.bcast(matrix2, root=0)
    rowsNum = comm.bcast(rowsNum, root=0)
    chunk = comm.scatter(chunks, root=0)

    chunkResult = multiply_matrices(chunk, matrix2)

    result = comm.gather(chunkResult, root=0)

    if rank == 0:
        # flatten the result
        result = [item for sublist in result for item in sublist]
        time_end = time()
        print(f"Time: {time_end - time_start} seconds")

if __name__ == "__main__":
    main()

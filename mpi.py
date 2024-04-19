import time

import numpy as np
from mpi4py import MPI

from generate_matrice_to_file import read_matrix_from_file


def save_matrix_to_file(matrix, filename):
    with open(filename, 'w') as file:
        for row in matrix:
            file.write(' '.join(map(str, row)) + '\n')


def multiply_matrices(matrix1, matrix2):
    return np.dot(matrix1, matrix2)


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    if rank == 0:
        matrix = read_matrix_from_file("matrix.txt")
        n = len(matrix)
        matrix1 = np.matrix(matrix)
        matrix2 = np.matrix(matrix)

        start_time = time.time()

        # розкидуєм по процесах
        comm.bcast(n, root=0)
        local_matrix1 = np.empty((n // size, n), dtype=int)
        comm.Scatter(matrix1, local_matrix1, root=0)

        matrix2 = comm.bcast(matrix2, root=0)

        local_result = multiply_matrices(local_matrix1, matrix2)


        global_result = None
        
        global_result = np.empty((n, n), dtype=int)
        comm.Gather(local_result, global_result, root=0)

        end_time = time.time()
        if rank == 0:
            print("Time mpi:", end_time - start_time, "seconds")
            save_matrix_to_file(global_result, "mpi_matrix.txt")

    else:
        n = comm.bcast(None, root=0)

        local_matrix1 = np.empty((n // size, n), dtype=int)

        comm.Scatter(None, local_matrix1, root=0)

        matrix2 = comm.bcast(None, root=0)

        local_result = multiply_matrices(local_matrix1, matrix2)
        comm.Gather(local_result, None, root=0)


if __name__ == "__main__":
    main()

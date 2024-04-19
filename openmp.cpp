#include <iostream>
#include <vector>
#include <omp.h>
#include <fstream>
#include <sstream>

// Function to multiply matrices
std::vector<std::vector<int>> multiplyMatrices(const std::vector<std::vector<int>> &matrix1, const std::vector<std::vector<int>> &matrix2)
{
    int N = matrix1.size();
    std::vector<std::vector<int>> result(N, std::vector<int>(N, 0));
#pragma omp parallel for collapse(2)
    for (int i = 0; i < N; ++i)
    {
        for (int j = 0; j < N; ++j)
        {
            for (int k = 0; k < N; ++k)
            {
                result[i][j] += matrix1[i][k] * matrix2[k][j];
            }
        }
    }
    return result;
}

std::vector<std::vector<int>> readMatrixFromFile(const std::string &filename)
{
    std::ifstream file(filename);
    std::vector<std::vector<int>> matrix;

    if (file.is_open())
    {
        std::string line;
        while (std::getline(file, line))
        {
            std::vector<int> row;
            std::istringstream iss(line);
            int num;
            while (iss >> num)
            {
                row.push_back(num);
            }
            matrix.push_back(row);
        }
        file.close();
    }
    else
    {
        std::cerr << "Unable to open file " << filename << std::endl;
    }

    return matrix;
}

int main()
{
    int N;
    std::string filename = "matrix.txt";

    std::vector<std::vector<int>> matrix1 = readMatrixFromFile(filename);
    std::vector<std::vector<int>> matrix2 = readMatrixFromFile(filename);

    N = matrix1.size();
    std::cout << N << std::endl;
    std::vector<std::vector<int>> result;

    double start_time = omp_get_wtime();
    result = multiplyMatrices(matrix1, matrix2);
    double end_time = omp_get_wtime();
    std::cout << "Time openmp: " << end_time - start_time << " seconds" << std::endl;

    std::ofstream outputFile("matrix_openmp.txt");

    if (!outputFile.is_open())
    {
        std::cerr << "Error: Unable to open file for writing." << std::endl;
        return 1;
    }

    for (const auto &row : result)
    {
        for (int elem : row)
        {
            outputFile << elem << " ";
        }
        outputFile << std::endl;
    }

    return 0;
}

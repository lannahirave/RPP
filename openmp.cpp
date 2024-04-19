#include <iostream>
#include <vector>
#include <omp.h>
#include <fstream>
#include <sstream>
using namespace std;


vector<vector<int>> multiplyMatrices(const vector<vector<int>> &matrix1, const vector<vector<int>> &matrix2)
{
    int N = matrix1.size();
    vector<vector<int>> result(N, vector<int>(N, 0));
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

vector<vector<int>> readMatrixFromFile(const string &filename)
{
    ifstream file(filename);
    vector<vector<int>> matrix;

    if (file.is_open())
    {
        string line;
        while (getline(file, line))
        {
            vector<int> row;
            istringstream iss(line);
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
        cerr << "Unable to open file " << filename << endl;
    }

    return matrix;
}

int main()
{
    int N;
    string filename = "matrix.txt";

    vector<vector<int>> matrix1 = readMatrixFromFile(filename);
    vector<vector<int>> matrix2 = readMatrixFromFile(filename);

    N = matrix1.size();
    cout << N << endl;
    vector<vector<int>> result;

    double start_time = omp_get_wtime();
    result = multiplyMatrices(matrix1, matrix2);
    double end_time = omp_get_wtime();
    cout << "Time openmp: " << end_time - start_time << " seconds" << endl;

    ofstream outputFile("matrix_openmp.txt");

    if (!outputFile.is_open())
    {
        cerr << "Error: Unable to open file for writing." << endl;
        return 1;
    }

    for (const auto &row : result)
    {
        for (int elem : row)
        {
            outputFile << elem << " ";
        }
        outputFile << endl;
    }

    return 0;
}

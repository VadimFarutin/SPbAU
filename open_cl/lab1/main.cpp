#pragma comment(lib, "OpenCL.lib")
#define __CL_ENABLE_EXCEPTIONS
#include <CL/cl.h>
#include "cl.hpp"

#include <vector>
#include <fstream>
#include <iostream>
#include <iterator>
#include <iomanip>
#include <algorithm>
#include <cmath>

int main() {
    std::freopen("input.txt", "r", stdin);
    std::freopen("output.txt", "w", stdout);

    size_t N, M;
    std::cin >> N >> M;

    size_t matrixASize = N * N;
    double *matrixA = new double[matrixASize];
    for (size_t i = 0; i < matrixASize; i++) {
        std::cin >> matrixA[i];
    }

    size_t matrixBSize = M * M;
    double *matrixB = new double[matrixBSize];
    for (size_t i = 0; i < matrixBSize; i++) {
        std::cin >> matrixB[i];
    }

    size_t convolutionMatrixSize = matrixASize;
    double *convolutionMatrix = new double[convolutionMatrixSize];
    std::fill(convolutionMatrix, convolutionMatrix + convolutionMatrixSize, 0);

    std::vector<cl::Platform> platforms;
    std::vector<cl::Device> devices;
    std::vector<cl::Kernel> kernels;

    try {
        // create platform
        cl::Platform::get(&platforms);
        platforms[0].getDevices(CL_DEVICE_TYPE_GPU, &devices);

        // create context
        cl::Context context(devices);

        // create command queue
        cl::CommandQueue queue(context, devices[0]);

        // load opencl source
        std::ifstream cl_file("convolution.cl");
        std::string cl_string(std::istreambuf_iterator<char>(cl_file),
                              (std::istreambuf_iterator<char>()));
        cl::Program::Sources source(1, std::make_pair(cl_string.c_str(), 
                                                      cl_string.length() + 1));

        // create program
        cl::Program program(context, source);

        // compile opencl source
        size_t const BLOCK_SIZE = 16;
        program.build(devices, "-D BLOCK_SIZE=" + BLOCK_SIZE);

        // allocate device buffers
        size_t matrixABufferSize = sizeof(double) * matrixASize;
        size_t matrixBBufferSize = sizeof(double) * matrixBSize;
        size_t convolutionMatrixBufferSize = sizeof(double) * convolutionMatrixSize;

        cl::Buffer dev_matrixA(context, CL_MEM_READ_ONLY, matrixABufferSize);
        cl::Buffer dev_matrixB(context, CL_MEM_READ_ONLY, matrixBBufferSize);
        cl::Buffer dev_convolutionMatrix(context, CL_MEM_WRITE_ONLY, convolutionMatrixBufferSize);

        // copy from cpu to gpu
        queue.enqueueWriteBuffer(dev_matrixA, CL_TRUE, 0, matrixABufferSize, matrixA);
        queue.enqueueWriteBuffer(dev_matrixB, CL_TRUE, 0, matrixBBufferSize, matrixB);

        // load named kernel from opencl source
        cl::Kernel convolutionKernel(program, "convolution");
        size_t block_cnt = (N + BLOCK_SIZE - 1) / BLOCK_SIZE;
        cl::KernelFunctor convolutionFunctor(convolutionKernel,
                                             queue,
                                             cl::NullRange,
                                             cl::NDRange(BLOCK_SIZE * block_cnt,
                                                         BLOCK_SIZE * block_cnt),
                                             cl::NDRange(BLOCK_SIZE, BLOCK_SIZE));
        convolutionFunctor(dev_matrixA, 
                           (int)N, 
                           dev_matrixB, 
                           (int)M, 
                           dev_convolutionMatrix);

        queue.enqueueReadBuffer(dev_convolutionMatrix,
                                CL_TRUE,
                                0,
                                convolutionMatrixBufferSize,
                                convolutionMatrix);

        std::cout.precision(3);
        std::cout << std::fixed;

        for (size_t i = 0; i < N; i++) {
            for (size_t j = 0; j < N; j++) {
                std::cout << convolutionMatrix[i * N + j] << ' ';
            }

            std::cout << std::endl;
        }
    }
    catch (cl::Error &e) {
        std::cout << std::endl << e.what() << " : " << e.err() << std::endl;
    }

    delete[] matrixA;
    delete[] matrixB;
    delete[] convolutionMatrix;

    return 0;
}

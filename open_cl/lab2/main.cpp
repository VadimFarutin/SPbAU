#pragma comment(lib, "OpenCL.lib")
#define __CL_ENABLE_EXCEPTIONS
#include <CL/cl.h>
#include "cl.hpp"

#include <vector>
#include <fstream>
#include <iostream>
#include <iterator>
#include <iomanip>
#include <assert.h>

void block_sums(std::vector<double> &scan_output,
                std::vector<double> &block_sums_output,
                size_t N, size_t block_size, size_t block_cnt,
                cl::Context &context, cl::Program &program, cl::CommandQueue &queue) {
    cl::Buffer dev_input(context, CL_MEM_READ_ONLY, sizeof(double) * N);
    cl::Buffer dev_output(context, CL_MEM_WRITE_ONLY, sizeof(double) * block_cnt);

    queue.enqueueWriteBuffer(dev_input, CL_TRUE, 0, sizeof(double) * N, scan_output.data());

    cl::Kernel kernel(program, "block_sums");
    cl::KernelFunctor block_sums_functor(kernel, 
                                         queue, 
                                         cl::NullRange, 
                                         cl::NDRange(block_cnt * block_size), 
                                         cl::NDRange(block_size));
    block_sums_functor(dev_input,
                       dev_output, 
                       (int)N,
                       (int)block_cnt);

    queue.enqueueReadBuffer(dev_output, CL_TRUE, 0, sizeof(double) * block_cnt, block_sums_output.data());
}

void add_block_sums(std::vector<double> &block_scan_output,
                    std::vector<double> &scan_output,
                    std::vector<double> &final_output,
                    size_t N, size_t block_size, size_t block_cnt,
                    cl::Context &context, cl::Program &program, cl::CommandQueue &queue) {
    cl::Buffer dev_block_input(context, CL_MEM_READ_ONLY, sizeof(double) * block_cnt);
    cl::Buffer dev_input(context, CL_MEM_READ_ONLY, sizeof(double) * N);
    cl::Buffer dev_output(context, CL_MEM_WRITE_ONLY, sizeof(double) * N);

    queue.enqueueWriteBuffer(dev_block_input, CL_TRUE, 0, sizeof(double) * block_cnt, block_scan_output.data());
    queue.enqueueWriteBuffer(dev_input, CL_TRUE, 0, sizeof(double) * N, scan_output.data());

    cl::Kernel kernel(program, "add_block_sums");
    cl::KernelFunctor add_functor(kernel,
                                  queue, 
                                  cl::NullRange, 
                                  cl::NDRange(block_cnt * block_size),
                                  cl::NDRange(block_size));
    add_functor(dev_block_input,
                dev_input, 
                dev_output, 
                (int)N);

    queue.enqueueReadBuffer(dev_output, CL_TRUE, 0, sizeof(double) * N, final_output.data());
}

void scan_hillis_steele_one_block(std::vector<double> &input,
                                  std::vector<double> &scan_output,
                                  size_t N, size_t block_size, size_t block_cnt,
                                  cl::Context &context, cl::Program &program, cl::CommandQueue &queue) {
    cl::Buffer dev_input(context, CL_MEM_READ_ONLY, sizeof(double) * N);
    cl::Buffer dev_output(context, CL_MEM_WRITE_ONLY, sizeof(double) * N);

    queue.enqueueWriteBuffer(dev_input, CL_TRUE, 0, sizeof(double) * N, input.data());

    cl::Kernel kernel(program, "scan_hillis_steele");
    cl::KernelFunctor scan_functor(kernel, 
                                   queue,
                                   cl::NullRange,
                                   cl::NDRange(block_cnt * block_size),
                                   cl::NDRange(block_size));
    scan_functor(dev_input,
                 dev_output,
                 cl::__local(sizeof(double) * block_size),
                 cl::__local(sizeof(double) * block_size),
                 (int)N);

    queue.enqueueReadBuffer(dev_output, CL_TRUE, 0, sizeof(double) * N, scan_output.data());
}

void scan_hillis_steele(std::vector<double> &input, 
                        std::vector<double> &scan_output, 
                        size_t N, 
                        cl::Context &context, cl::Program &program, cl::CommandQueue &queue) {
    size_t const block_size = 256;
    size_t block_cnt = (N + block_size - 1) / block_size;

    scan_hillis_steele_one_block(input, scan_output, N, block_size, block_cnt, context, program, queue);

    if (N > block_size) {
        std::vector<double> block_sums_output(block_cnt, 0);
        std::vector<double> block_scan_output(block_cnt, 0);
        std::vector<double> final_output(N, 0);

        block_sums(scan_output, block_sums_output, N, block_size, block_cnt, context, program, queue);
        scan_hillis_steele(block_sums_output, block_scan_output, block_cnt, context, program, queue);
        add_block_sums(block_scan_output, scan_output, final_output, N, block_size, block_cnt, context, program, queue);

        scan_output = final_output;
    }
}

int main() {
    std::freopen("input.txt", "r", stdin);
    std::freopen("output.txt", "w", stdout);
    
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
        cl::CommandQueue queue(context, devices[0], CL_QUEUE_PROFILING_ENABLE);

        // load opencl source
        std::ifstream cl_file("scan.cl");
        std::string cl_string(std::istreambuf_iterator<char>(cl_file), (std::istreambuf_iterator<char>()));
        cl::Program::Sources source(1, std::make_pair(cl_string.c_str(), cl_string.length() + 1));

        // create program
        cl::Program program(context, source);

        // compile opencl source
        program.build(devices);

        // create a message to send to kernel
        size_t N;
        std::cin >> N;

        std::vector<double> input(N);
        std::vector<double> output(N, 0);

        for (size_t i = 0; i < N; i++) {
            std::cin >> input[i];
        }

        scan_hillis_steele(input, output, N, context, program, queue);

        std::cout.precision(3);
        std::cout << std::fixed;

        for (size_t i = 0; i < N; i++) {
            std::cout << output[i] << ' ';
        }
    } catch (cl::Error e) {
        std::cout << std::endl << e.what() << " : " << e.err() << std::endl;
    }

    return 0;
}

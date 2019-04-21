__kernel void convolution(
    __global double *matrixA,
    int N,
    __global double *matrixB,
    int M,
    __global double *convolutionMatrix) 
{
    int i = get_global_id(0);
    int j = get_global_id(1);

    if (i >= N || j >= N) {
        return;
    }

    int HM = (M - 1) / 2;
    double sum = 0;
    
    for (int k = -HM; k <= HM; k++) {
        for (int l = -HM; l <= HM; l++) {
            if (i + k < 0 || j + l < 0 || i + k >= N || j + l >= N) {
                continue;
            }

            sum += matrixA[(i + k) * N + (j + l)] *
                   matrixB[(k + HM) * M + (l + HM)];
        }
    }

    convolutionMatrix[i * N + j] = sum;
}

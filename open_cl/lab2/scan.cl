#define SWAP(a,b) {__local double * tmp=a; a=b; b=tmp;}

__kernel void scan_hillis_steele(__global double * input,
                                 __global double * output, 
                                 __local double * a, 
                                 __local double * b,
                                 int n) {
    uint gid = get_global_id(0);
    uint lid = get_local_id(0);
    uint block_size = get_local_size(0);

    if (gid < n) {
        a[lid] = b[lid] = input[gid];
    }

    barrier(CLK_LOCAL_MEM_FENCE);

    for (uint s = 1; s < block_size; s <<= 1) {
        if (lid > (s - 1)) {
            b[lid] = a[lid] + a[lid - s];
        }
        else {
            b[lid] = a[lid];
        }

        barrier(CLK_LOCAL_MEM_FENCE);
        SWAP(a, b);
    }

    if (gid < n) {
        output[gid] = a[lid];
    }
}

__kernel void block_sums(__global double *input, 
                         __global double *output,
                         int n, 
                         int m) {
    uint gid = get_global_id(0);
    uint block_size = get_local_size(0);
    uint i = gid / block_size;

    if (gid < n && i < m && (gid == (i + 1) * block_size - 1 || gid == n - 1)) {
        output[i] = input[gid];
    }
}

__kernel void add_block_sums(__global double *block_sums, 
                             __global double *input,
                             __global double *output, 
                             int n) {
    uint gid = get_global_id(0);
    uint block_size = get_local_size(0);
    uint i = gid / block_size;

    if (gid < n) {
        if (i >= 1) {
            output[gid] = input[gid] + block_sums[i - 1];
        }
        else {
            output[gid] = input[gid];
        }
    }
}

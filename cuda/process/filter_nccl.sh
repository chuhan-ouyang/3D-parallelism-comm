#!/bin/bash
# python3 filter_nccl.py ../traces/node0_cuda_gpu_trace_rank0.csv ../traces/node0_cuda_gpu_trace_rank0.csv
python3 filter_nccl.py ../traces/node1_cuda_gpu_trace_rank0.csv ../traces/node1_cuda_gpu_trace_rank0.csv
python3 filter_nccl.py ../traces/node2_cuda_gpu_trace_rank0.csv ../traces/node2_cuda_gpu_trace_rank0.csv
python3 filter_nccl.py ../traces/node3_cuda_gpu_trace_rank0.csv ../traces/node3_cuda_gpu_trace_rank0.csv
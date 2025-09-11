#!/bin/bash
# python3 separate_cuda_ranks.py ../traces/node0_cuda_gpu_trace.csv
python3 separate_cuda_ranks.py ../traces/node1_cuda_gpu_trace.csv
python3 separate_cuda_ranks.py ../traces/node2_cuda_gpu_trace.csv
python3 separate_cuda_ranks.py ../traces/node3_cuda_gpu_trace.csv
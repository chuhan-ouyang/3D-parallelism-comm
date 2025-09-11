#!/bin/bash
# python3 remove_tp_na.py \
#     ../traces/node0_cuda_gpu_trace_rank0_labeled.csv \

python3 remove_tp_na.py \
    ../traces/node0_cuda_gpu_trace_rank0_labeled.csv \

python3 remove_tp_na.py \
    ../traces/node1_cuda_gpu_trace_rank0_labeled.csv \

python3 remove_tp_na.py \
    ../traces/node2_cuda_gpu_trace_rank0_labeled.csv \

python3 remove_tp_na.py \
    ../traces/node3_cuda_gpu_trace_rank0_labeled.csv \
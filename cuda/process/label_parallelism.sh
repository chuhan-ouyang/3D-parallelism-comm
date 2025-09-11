#!/bin/bash
# python3 label_parallelism.py \
# ../../nvtx/traces/node0_nvtx_events_rank0_labeled.csv \
# ../traces/node0_cuda_gpu_trace_rank0.csv \

python3 label_parallelism.py \
../../nvtx/traces/node1_nvtx_events_rank0_labeled.csv \
../traces/node1_cuda_gpu_trace_rank0.csv \

python3 label_parallelism.py \
../../nvtx/traces/node2_nvtx_events_rank0_labeled.csv \
../traces/node2_cuda_gpu_trace_rank0.csv \

python3 label_parallelism.py \
../../nvtx/traces/node3_nvtx_events_rank0_labeled.csv \
../traces/node3_cuda_gpu_trace_rank0.csv \
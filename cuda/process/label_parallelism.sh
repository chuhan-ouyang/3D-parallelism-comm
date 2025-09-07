#!/bin/bash
python3 label_parallelism.py \
traces/node1_nvtx_pushpop_trace_pid_964832_all_labeled.csv \
traces/node1_cuda_gpu_trace_local_rank_0_filtered.csv \

python3 label_parallelism.py \
traces/node3_nvtx_pushpop_trace_pid_951286_all_labeled.csv \
traces/node3_cuda_gpu_trace_local_rank_0_filtered.csv \

# python3 label_parallelism.py \
# /global/homes/c/co232/ReCCL-workspace/torchtitan/windows/nsys/nvtx/traces/node0_nvtx_pushpop_trace_pid_1114945_all_labeled.csv \
# traces/node0_cuda_gpu_trace_local_rank_0_filtered.csv \

# python3 label_parallelism.py \
# /global/homes/c/co232/ReCCL-workspace/torchtitan/windows/nsys/nvtx/traces/node2_nvtx_pushpop_trace_pid_563290_all_labeled.csv \
# traces/node2_cuda_gpu_trace_local_rank_0_filtered.csv \
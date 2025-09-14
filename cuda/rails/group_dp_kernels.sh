#!/usr/bin/env bash

NODE0="../traces/node0_cuda_gpu_trace_rank0_labeled_dp_pp_synch.csv"
NODE1="../traces/node1_cuda_gpu_trace_rank0_labeled_dp_pp_synch.csv"
NODE2="../traces/node2_cuda_gpu_trace_rank0_labeled_dp_pp_synch.csv"
NODE3="../traces/node3_cuda_gpu_trace_rank0_labeled_dp_pp_synch.csv"

python3 group_dp_kernels.py "$NODE0"
python3 group_dp_kernels.py "$NODE1"
python3 group_dp_kernels.py "$NODE2"
python3 group_dp_kernels.py "$NODE3"

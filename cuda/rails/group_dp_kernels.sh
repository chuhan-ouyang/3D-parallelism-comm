#!/usr/bin/env bash

NODE0="/global/homes/c/co232/ReCCL-workspace/torchtitan/windows/nsys/cuda/traces/node0_cuda_gpu_trace_local_rank_0_filtered_labeled_dp_pp.csv"
NODE1="/global/homes/c/co232/ReCCL-workspace/torchtitan/windows/nsys/cuda/traces/node1_cuda_gpu_trace_local_rank_0_filtered_labeled_dp_pp_synch.csv"
NODE2="/global/homes/c/co232/ReCCL-workspace/torchtitan/windows/nsys/cuda/traces/node2_cuda_gpu_trace_local_rank_0_filtered_labeled_dp_pp_synch.csv"
NODE3="/global/homes/c/co232/ReCCL-workspace/torchtitan/windows/nsys/cuda/traces/node3_cuda_gpu_trace_local_rank_0_filtered_labeled_dp_pp_synch.csv"


python3 group_by_parallelism.py "$NODE0"
python3 group_by_parallelism.py "$NODE1"
python3 group_by_parallelism.py "$NODE2"
python3 group_by_parallelism.py "$NODE3"

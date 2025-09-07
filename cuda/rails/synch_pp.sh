#!/usr/bin/env bash

BASE="/global/homes/c/co232/ReCCL-workspace/torchtitan/windows/nsys/cuda/traces/node1_cuda_gpu_trace_local_rank_0_filtered_labeled_dp_pp_synch.csv"
OTHER="/global/homes/c/co232/ReCCL-workspace/torchtitan/windows/nsys/cuda/traces/node3_cuda_gpu_trace_local_rank_0_filtered_labeled_dp_pp.csv"

python3 synch_pp.py "$BASE" "$OTHER"

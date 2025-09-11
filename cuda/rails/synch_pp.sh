#!/usr/bin/env bash

BASE="../traces/node0_cuda_gpu_trace_rank0_labeled_dp_pp.csv"
OTHER="../traces/node2_cuda_gpu_trace_rank0_labeled_dp_pp.csv"

python3 synch_pp.py "$BASE" "$OTHER"

BASE1="../traces/node1_cuda_gpu_trace_rank0_labeled_dp_pp_synch.csv"
OTHER1="../traces/node3_cuda_gpu_trace_rank0_labeled_dp_pp.csv"

python3 synch_pp.py "$BASE1" "$OTHER1"

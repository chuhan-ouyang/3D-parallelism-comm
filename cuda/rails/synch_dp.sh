#!/usr/bin/env bash

BASE="../traces/node0_cuda_gpu_trace_rank0_labeled_dp_pp.csv"
OTHER="../traces/node1_cuda_gpu_trace_rank0_labeled_dp_pp.csv"

python3 synch_dp.py "$BASE" "$OTHER"

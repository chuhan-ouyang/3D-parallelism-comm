#!/bin/bash
# python3 calc_wind.py traces/node1_cuda_gpu_trace_local_rank_0_filtered_labeled_dp_pp.csv traces/rank4_windows.csv
# python3 calc_wind.py traces/node3_cuda_gpu_trace_local_rank_0_filtered_labeled_dp_pp.csv traces/rank12_windows.csv
python3 calc_wind.py ../traces/node0_cuda_gpu_trace_rank0_labeled_dp_pp_grouped.csv ../traces/node0_rank0_windows.csv
# python3 calc_wind.py traces/node2_cuda_gpu_trace_local_rank_0_filtered_labeled_dp_pp.csv traces/rank8_windows.csv

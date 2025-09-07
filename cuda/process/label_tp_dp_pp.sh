#!/bin/bash

# Rank4
python3 label_tp_dp_pp.py traces/node1_nvtx_pushpop_trace_pid_964832.csv

# Rank12
python3 label_tp_dp_pp.py traces/node3_nvtx_pushpop_trace_pid_951286.csv

# Rank0
# python3 label_tp_dp_pp.py traces/node0_nvtx_pushpop_trace_pid_1114945.csv

# Rank8
# python3 label_tp_dp_pp.py traces/node2_nvtx_pushpop_trace_pid_563290.csv
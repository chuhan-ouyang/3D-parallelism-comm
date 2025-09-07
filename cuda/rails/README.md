# Per-Rail Window Size Calculation

#### Time Synch
Using files: node0_cuda_gpu_trace_local_rank_0_filtered_labeled_dp_pp.csv, node1_cuda_gpu_trace_local_rank_0_filtered_labeled_dp_pp.csv, node2_cuda_gpu_trace_local_rank_0_filtered_labeled_dp_pp.csv, node3_cuda_gpu_trace_local_rank_0_filtered_labeled_dp_pp.csv (see process/README.md)

1. synch_dp.sh/synch_dp.py: synch other to base usign first A/G kernel end time -> _synch.csv
Synch rank4 to rank0 
2. synch_pp.sh/synch_pp.py: synch other to base using first S/R kernel end time -> _synch.csv
Synch rank8 to rank0
Synch rank12 to rank4

#### Group Kernels
1. group_dp_kernels.sh/group_dp kernels.py: combine all kernels of the same DP type, record kernel names

#### OCS Schedule
1. calc_ocs_circuit.sh/calc_ocs_circuit.py


#### OCS Per-Rail Window Size
1. calc_ocs_global_wind.sh/calc_ocs_global_wind.py
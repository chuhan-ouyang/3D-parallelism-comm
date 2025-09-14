# Per-Rail Window Size Calculation

#### Time Synch
Using files: ../traces:
node0_cuda_gpu_trace_rank0_labeled_dp_pp.csv
node1_cuda_gpu_trace_rank0_labeled_dp_pp.csv
node2_cuda_gpu_trace_rank0_labeled_dp_pp.csv
node3_cuda_gpu_trace_rank0_labeled_dp_pp.csv

1. synch_dp.sh/synch_dp.py: synch other to base usign first A/G kernel end time -> _synch.csv
Synch rank4(node1) to rank0(node0)
2. synch_pp.sh/synch_pp.py: synch other to base using first S/R kernel end time -> _synch.csv
Synch rank8(node2) to rank0(node0)
Synch rank12(node3) to rank4(node1 synched version)

Result Example:
Base - Other Offset: 252905748 ns
Wrote synched CSV: ../traces/node1_cuda_gpu_trace_rank0_labeled_dp_pp_synch.csv

Base - Other Offset: 523898832 ns
Wrote synched CSV: ../traces/node2_cuda_gpu_trace_rank0_labeled_dp_pp_synch.csv

Base - Other Offset: 586259512 ns
Wrote synched CSV: ../traces/node3_cuda_gpu_trace_rank0_labeled_dp_pp_synch.csv

#### Group Kernels
1. group_dp_kernels.sh/group_dp_kernels.py (for each rank): combine all kernels of the same DP type, record kernel names. Aggregate sizes. Group consecutive DP kernels; pass PP rows through. We only group DP kernels because for calculating OCS circuit, PP rows need to be synched among the 4 ranks, DP ros are synched among 2 ranks of te DP group (rank0 and 4, rank 8 and 12).

#### OCS Schedule
1. calc_ocs_circuit.sh/calc_ocs_circuit.py
Note: mv ../traces/node0_cuda_gpu_trace_rank0_labeled_dp_pp_grouped.csv ../traces/node0_cuda_gpu_trace_rank0_labeled_dp_pp_synch_grouped.csv for naming conventions 

PP circuits calculated across all 4 nodes: max(4 nodes start) to max(4 nodes end)

DP circuits calculated per pipeline stage (nodes[:2] and nodes[2:]): max(2 nodes start) to max(2 nodes end)

Circuit's communication size = sum of communication sizes of all participating ranks' kernels

Sort all circuits by end time

#### OCS Per-Rail Window Size
1. calc_ocs_global_wind.sh/calc_ocs_global_wind.py
If switch from DP - PP or PP - DP then calcualte window size. Record size of kernel after.
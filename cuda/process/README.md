# CUDA GPU Trace Processing

Raw nsys rep files in :/pscratch/sd/c/co232/nsys_tp_4_dp_2_shard_pp_2_10itrs_nccl2.27_nsys2025-3

# Export CUDA trace from nsys
1. export CUDA kernels:
```bash
./run_gen_cuda.sh
```

## Process corresponding NVTX trace for parallelism labeling
See ../../nvtx/README.med

## Process CUDA trace
1. separate_cuda_ranks.py/separate_cuda_ranks.sh
Separate based on CUDA device -> rank0.csv
Only keep rank 0 (as needed for rails analysis)

2. filter_nccl.sh/filter_nccl.py
Only keep NCCL events -> _rank0.csv (overwrite step1)

3. label_parallelism.sh/label_parallelism.py
Reference nvtx trace's TP/DP labeling (based on comm ID), label the cuda GPU trace assuming the same parallelism orders. Populate a Communication Size (bytes) field based on nvtx corresponding kernel's size. PP size: 16777216 bytes -> rank0_labeled.csv

4. remove_tp_na.sh/remove_tp_na.py: remove TP, NA -> rank0_labeled_dp_pp.csv

## Per-Rank Window Calculaion
1. group_parallelism.sh/group_parallelism.py: group all kernels of the same parallelism type to record start, end, duration, start kernel name, end kernel name, total bytes 0 -> rank0_labeled_dp_pp_grouped.csv
2. calc_wind.sh/calc_wind.py: calculate per-rank window sizes and aggregarate message size (bytes) for all kernels after a switching window. -> node0_rank0_windows.csv
3. ipynb for plot: windows cdf + size vs. windows graph
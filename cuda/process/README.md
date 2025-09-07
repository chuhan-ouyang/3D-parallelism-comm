# CUDA GPU Trace Processing

Raw nsys rep files in :/pscratch/sd/c/co232/nsys_tp_4_dp_2_shard_pp_2_10itrs_nccl2.27_nsys2025-3

## Process corresponding NVTX trace for parallelism labeling (using groupStart/End)
1. separate_ranks.sh/separate_ranks.py -> _pid_x.csv 
2. label_tp_dp_pp.sh/label_tp_dp_pp.py -> _all_labeled.csv

## Process CUDA trace
1. separate_cuda_ranks.py/separate_cuda_ranks.sh
Separate based on CUDA device -> local_rank_x.csv

2. filter_nccl.sh/filter_nccl.py
Only keep NCCL events -> _filtered.csv

3. label_parallelism.sh/label_parallelism.py
Reference nvtx trace's TP/DP labeling (based on presence of groupStart/End wrapping), label the cuda GPU trace assuming the same parallelism orders -> _filtered_labeled.csv

nvtx's all_labeled vs cuda's filtered

4. remove_tp_na.sh/remove_tp_na.py: remove TP, NA -> _dp_pp.csv

5. calc_wind.sh/calc_wind.py:calculate per-rank window sizes

6. ipynb for plot
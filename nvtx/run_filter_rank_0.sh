#!/bin/bash
# run_filter_rank_0.sh
# Usage:
#   ./run_filter_rank_0.sh traces/node0_nvtx_events.csv 300180650918721 300180650919336

set -euo pipefail

# Filter rank 0 of node 0
# globalTid=300180650918721 -> PID=1114945, TID=1114945
# globalTid=300180650919336 -> PID=1114945, TID=1115560
# python filter_rank_0.py traces/node0_nvtx_events.csv 300180650918721 300180650919336

# Filter rank 0 of node 1
# globalTid=297662172543200 -> PID=964832, TID=964832
# globalTid=297662172543802 -> PID=964832, TID=965434
python filter_rank_0.py traces/node1_nvtx_events.csv 297662172543200 297662172543802

# Filter rank 0 of node 2
# globalTid=290925415274586 -> PID=563290, TID=563290
# globalTid=290925415275177 -> PID=563290, TID=563881
python filter_rank_0.py traces/node2_nvtx_events.csv 290925415274586 290925415275177

# Filter rank 0 of node 3
# globalTid=297434908361718 -> PID=951286, TID=951286
# globalTid=297434908362308 -> PID=951286, TID=951876
python filter_rank_0.py traces/node3_nvtx_events.csv 297434908361718 297434908362308
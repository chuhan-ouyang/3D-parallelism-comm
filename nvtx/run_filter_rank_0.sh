#!/bin/bash
# run_filter_rank_0.sh
# Usage:
#   ./run_filter_rank_0.sh traces/node0_nvtx_events.csv 300180650918721 300180650919336

set -euo pipefail

# Filter rank 0 of node 0
# globalTid=300180650918721 -> PID=1114945, TID=1114945
# globalTid=300180650919336 -> PID=1114945, TID=1115560
python filter_rank_0.py traces/node0_nvtx_events.csv 300180650918721 300180650919336

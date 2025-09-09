#!/bin/bash
# run_label_parallelism.sh
# Usage:
#   ./run_label_parallelism.sh node0_nvtx_events_rank0.csv dp tp ppsend pprecv

set -euo pipefail

python label_parallelism.py traces/node0_nvtx_events_rank0.csv \
  "3574919951526054331" \
  "18319673707052330093" \
  "6004158948986910404" \
  "6831535697949778466"

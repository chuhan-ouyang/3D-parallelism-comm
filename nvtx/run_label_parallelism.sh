#!/bin/bash
# run_label_parallelism.sh
# Usage:
#   ./run_label_parallelism.sh node0_nvtx_events_rank0.csv dp tp ppsend pprecv

set -euo pipefail

# python label_parallelism.py traces/node0_nvtx_events_rank0.csv \
#   "3574919951526054331" \
#   "18319673707052330093" \
#   "6004158948986910404" \
#   "6831535697949778466"

python label_parallelism.py traces/node1_nvtx_events_rank0.csv \
  "3574919951526054331" \
  "454674816390077854" \
  "2194994131262233267" \
  "16862997107819585018"

python label_parallelism.py traces/node2_nvtx_events_rank0.csv \
  "18316173711765036671" \
  "2189860248865579961" \
  "6831535697949778466" \
  "6004158948986910404"

python label_parallelism.py traces/node3_nvtx_events_rank0.csv \
  "18316173711765036671" \
  "17041003602900097456" \
  "16862997107819585018" \
  "2194994131262233267"

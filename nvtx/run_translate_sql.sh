#!/usr/bin/env bash
# run_translate_sql.sh
# Usage: ./run_translate_sql.sh

set -euo pipefail

# python3 translate_sql.py -i INPUT_DB="../nsys/0_41047697_json.sqlite" -o OUTPUT_CSV="traces/node0_nvtx_events.csv"
python3 translate_sql.py -i "../nsys/1_41047697_json.sqlite" -o "traces/node1_nvtx_events.csv"
python3 translate_sql.py -i "../nsys/2_41047697_json.sqlite" -o "traces/node2_nvtx_events.csv"
python3 translate_sql.py -i "../nsys/3_41047697_json.sqlite" -o "traces/node3_nvtx_events.csv"

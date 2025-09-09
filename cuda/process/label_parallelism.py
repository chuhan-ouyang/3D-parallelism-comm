#!/usr/bin/env python3
import argparse
import os
import json
import pandas as pd
import math
import sys

def parse_args():
    p = argparse.ArgumentParser(
        description="Label TP/DP for DevKernel trace based on NCCL trace"
    )
    p.add_argument(
        'nvtxevents',
        help="CSV file with NCCL event logs (contains kernel_name and Parallelism columns)"
    )
    p.add_argument(
        'devkernels',
        help="CSV file with device kernel logs (Name to be labeled)"
    )
    p.add_argument(
        '-o', '--output',
        help="Output CSV file for labeled devkernels (default: devkernels_labeled.csv)",
        default=None
    )
    return p.parse_args()

def parse_json_text(val):
    """Return dict from jsonText cell or {} if missing/unparseable."""
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return {}
    if isinstance(val, str):
        s = val.strip()
        if not s:
            return {}
        try:
            # Many CSV writers already escape inner quotes correctly; try direct loads first.
            return json.loads(s)
        except Exception:
            # Fallback: sometimes doubled quotes leak through
            try:
                return json.loads(s.replace("''", '"').replace('""', '"'))
            except Exception:
                return {}
    return {}

def coerce_size_bytes(x):
    """Coerce numeric size to int string; else return 'NA'."""
    if x is None:
        return 'NA'
    try:
        # Some payloads may store as float; cast down safely.
        return str(int(x))
    except Exception:
        return 'NA'

def main():
    args = parse_args()
    # Determine output path
    dev_path = args.devkernels
    out_path = args.output or os.path.splitext(dev_path)[0] + '_labeled.csv'
    print("try read nvtx")
    # Read NCCL events
    try:
        df_n = pd.read_csv(args.nvtxevents)
    except Exception as e:
        print(f"Error reading NCCL events file: {e}", file=sys.stderr)
        sys.exit(1)
    print("finish reading nvtx")

    required_nvtx_cols = {'kernel_name', 'Parallelism', 'jsonText'}
    missing = required_nvtx_cols - set(df_n.columns)
    if missing:
        print(f"Error: NVTX CSV missing columns: {sorted(missing)}", file=sys.stderr)
        sys.exit(1)
    print("checked nvtx")

    # Build label and size dictionaries
    ag_map = {}
    rs_map = {}
    ag_idx = 0
    rs_idx = 0
    for _, row in df_n.iterrows():
        kname = str(row.get('kernel_name', '') or '')
        par   = str(row.get('Parallelism', '') or 'NA')
        j     = parse_json_text(row.get('jsonText'))

        if kname == 'ncclAllGather':
            size = coerce_size_bytes(j.get('Message size [bytes]'))
            ag_map[ag_idx] = (par, size)
            ag_idx += 1
        elif kname == 'ncclReduceScatter':
            size = coerce_size_bytes(j.get('Message size [bytes]'))
            rs_map[rs_idx] = (par, size)
            rs_idx += 1
        # ignore other nvtx rows
    print("build ag rs map")

    # Read device kernel trace
    try:
        df_d = pd.read_csv(dev_path)
    except Exception as e:
        print(f"Error reading device kernels file: {e}", file=sys.stderr)
        sys.exit(1)
    
    if 'Name' not in df_d.columns:
        print("Error: device kernels CSV must contain a 'Name' column.", file=sys.stderr)
        sys.exit(1)

    # Label dev kernels
    ag_count = 0
    rs_count = 0
    labels = []
    sizes  = []

    for _, row in df_d.iterrows():
        name = str(row.get('Name', '') or '')

        if name.startswith('ncclDevKernel_AllGather'):
            par, size = ag_map.get(ag_count, ('NA', 'NA'))
            if par == 'NA':
                print(f"Warning: no NVTX label/size for AllGather index {ag_count}", file=sys.stderr)
            labels.append(par)
            sizes.append(size)
            ag_count += 1

        elif name.startswith('ncclDevKernel_ReduceScatter'):
            par, size = rs_map.get(rs_count, ('NA', 'NA'))
            if par == 'NA':
                print(f"Warning: no NVTX label/size for ReduceScatter index {rs_count}", file=sys.stderr)
            labels.append(par)
            sizes.append(size)
            rs_count += 1

        elif name.startswith('ncclDevKernel_SendRecv'):
            # Pipeline kernels → label PP and fixed size 16MiB
            labels.append('PP')
            sizes.append(str(16777216))

        else:
            labels.append('NA')
            sizes.append('NA')

    # Add column and write
    df_d['Parallelism'] = labels
    df_d['Size(bytes)'] = sizes

    df_d.to_csv(out_path, index=False)
    print(f"Wrote labeled devkernel events with sizes to {out_path}")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import argparse
import os
import pandas as pd
import sys

def parse_args():
    p = argparse.ArgumentParser(
        description="Label TP/DP for DevKernel trace based on NCCL trace"
    )
    p.add_argument(
        'nvtxevents',
        help="CSV file with NCCL event logs (contains Name and Parallelism columns)"
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


def main():
    args = parse_args()
    # Determine output path
    dev_path = args.devkernels
    out_path = args.output or os.path.splitext(dev_path)[0] + '_labeled.csv'

    # Read NCCL events
    try:
        df_n = pd.read_csv(args.nvtxevents)
    except Exception as e:
        print(f"Error reading NCCL events file: {e}", file=sys.stderr)
        sys.exit(1)

    # Build label dictionaries
    allgather_labels = {}
    reducescatter_labels = {}
    ag_idx = 0
    rs_idx = 0
    for _, row in df_n.iterrows():
        name = row.get('Name', '')
        pl = row.get('Parallelism', '')
        if name == 'NCCL:ncclAllGather':
            allgather_labels[ag_idx] = pl
            ag_idx += 1
        elif name == 'NCCL:ncclReduceScatter':
            reducescatter_labels[rs_idx] = pl
            rs_idx += 1

    # Read device kernel trace
    try:
        df_d = pd.read_csv(dev_path)
    except Exception as e:
        print(f"Error reading device kernels file: {e}", file=sys.stderr)
        sys.exit(1)

    # Label dev kernels
    ag_count = 0
    rs_count = 0
    labels = []
    for _, row in df_d.iterrows():
        name = row.get('Name', '')
        if name.startswith('ncclDevKernel_AllGather'):
            if ag_count not in allgather_labels:
                print(f"Warning: no label for AllGather index {ag_count}", file=sys.stderr)
                lab = 'NA'
            else:
                lab = allgather_labels[ag_count]
            ag_count += 1
        elif name.startswith('ncclDevKernel_ReduceScatter'):
            if rs_count not in reducescatter_labels:
                print(f"Warning: no label for ReduceScatter index {rs_count}", file=sys.stderr)
                lab = 'NA'
            else:
                lab = reducescatter_labels[rs_count]
            rs_count += 1
        elif name.startswith('ncclDevKernel_SendRecv'):
            lab = 'PP'
        else:
            lab = 'NA'
        labels.append(lab)

    # Add column and write
    df_d['Parallelism'] = labels
    df_d.to_csv(out_path, index=False)
    print(f"Wrote labeled devkernel events to {out_path}")


if __name__ == '__main__':
    main()

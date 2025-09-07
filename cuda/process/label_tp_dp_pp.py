#!/usr/bin/env python3
import argparse
import pandas as pd
import sys

def parse_args():
    p = argparse.ArgumentParser(
        description="Label NCCL events with parallelism type"
    )
    p.add_argument(
        "input",
        help="Input CSV file with a 'Name' column"
    )
    p.add_argument(
        "-o", "--output",
        help="Output CSV file",
        default=None
    )
    return p.parse_args()

def main():
    args = parse_args()
    df = pd.read_csv(args.input)

    # match nested groupStart/groupEnd using a stack
    stack = []
    pairs = []  # list of (start_idx, end_idx)
    for idx, name in df['Name'].items():
        if name == 'NCCL:ncclGroupStart':
            stack.append(idx)
        elif name == 'NCCL:ncclGroupEnd':
            if stack:
                start_idx = stack.pop()
                pairs.append((start_idx, idx))
            else:
                print(f"Warning: unmatched NCCL:ncclGroupEnd at row {idx}", file=sys.stderr)
    if stack:
        for s in stack:
            print(f"Warning: unmatched NCCL:ncclGroupStart at row {s}", file=sys.stderr)

    def enclosed(idx):
        # True if idx is strictly inside any (start, end)
        return any(s < idx < e for s, e in pairs)

    labels = []
    for idx, name in df['Name'].items():
        if name in ('NCCL:ncclSend', 'NCCL:ncclRecv'):
            labels.append('PP')
        elif name in ('NCCL:ncclAllGather', 'NCCL:ncclReduceScatter'):
            labels.append('TP' if enclosed(idx) else 'DP')
        else:
            labels.append('NA')

    df['Parallelism'] = labels

    out_path = args.output or args.input.replace('.csv', '_all_labeled.csv')
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} rows with Parallelism labels to {out_path}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import os
import re
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(
        description="Split a CUDA trace CSV by device-local rank parsed from the Device column"
    )
    parser.add_argument(
        "input_csv",
        help="Path to the input CSV with a 'Device' column like 'NVIDIA A100-SXM4-40GB (0)' and 'Start (ns)'"
    )
    args = parser.parse_args()
    input_csv = args.input_csv

    # Prepare paths
    input_path = os.path.abspath(input_csv)
    input_dir = os.path.dirname(input_path)
    base_name = os.path.splitext(os.path.basename(input_csv))[0]

    # Read CSV
    df = pd.read_csv(input_csv)

    # Check required columns
    if "Device" not in df.columns or "Start (ns)" not in df.columns:
        print("Error: input file must contain 'Device' and 'Start (ns)' columns")
        return

    # Extract local rank number from Device, e.g. "(2)" -> 2
    df["local_rank"] = df["Device"].str.extract(r"\((\d+)\)")
    missing = df["local_rank"].isna().sum()
    if missing > 0:
        print(f"Warning: {missing} rows where Device did not match pattern; they will be skipped")
    df = df.dropna(subset=["local_rank"])
    df["local_rank"] = df["local_rank"].astype(int)

    # Identify unique ranks
    ranks = sorted(df["local_rank"].unique())
    print("Found local ranks:", ", ".join(str(r) for r in ranks))
    if len(ranks) != 4:
        print(f"Warning: expected 4 distinct ranks but found {len(ranks)}")

    # Split and write
    for r in ranks:
        subset = df[df["local_rank"] == r].sort_values("Start (ns)")
        output_filename = f"{base_name}_local_rank_{r}.csv"
        output_path = os.path.join(input_dir, output_filename)
        subset.to_csv(output_path, index=False)
        print(f"Wrote {len(subset)} rows for local_rank {r} to {output_path}")

if __name__ == "__main__":
    main()
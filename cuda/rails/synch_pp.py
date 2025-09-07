#!/usr/bin/env python3
import argparse
import os
import sys
import pandas as pd

TARGET_NAME = "ncclDevKernel_SendRecv(ncclDevKernelArgsStorage<(unsigned long)4096>)"
TARGET_PARALLELISM = "PP"

def first_endtime(csv_path: str) -> int:
    df = pd.read_csv(csv_path)
    df["Start (ns)"] = df["Start (ns)"].apply(int)
    df["Duration (ns)"] = df["Duration (ns)"].apply(int)

    m = (df["Name"] == TARGET_NAME) & (df["Parallelism"] == TARGET_PARALLELISM)
    hit = df[m]
    if hit.empty:
        print(f"ERROR: No matching row in {csv_path} for Name='{TARGET_NAME}' and Parallelism='{TARGET_PARALLELISM}'", file=sys.stderr)
        sys.exit(1)

    row = hit.iloc[0]
    return int(row["Start (ns)"]) + int(row["Duration (ns)"])

def make_output_path(input_path: str) -> str:
    root, ext = os.path.splitext(input_path)
    return f"{root}_synch{ext or ''}"

def main():
    ap = argparse.ArgumentParser(description="Sync 'other' CSV PP timing to 'base' by shifting Start (ns).")
    ap.add_argument("base_csv", help="Path to base CSV")
    ap.add_argument("other_csv", help="Path to other CSV to be shifted")
    args = ap.parse_args()

    base_end = first_endtime(args.base_csv)
    other_end = first_endtime(args.other_csv)
    offset = base_end - other_end
    print(f"Base - Other Offset: {offset} ns")

    df_other = pd.read_csv(args.other_csv)
    df_other["Start (ns)"] = df_other["Start (ns)"].apply(int) + int(offset)

    out_path = make_output_path(args.other_csv)
    df_other.to_csv(out_path, index=False)
    print(f"Wrote synched CSV: {out_path}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import os
import sys
import pandas as pd

def make_output_path(input_path: str) -> str:
    root, ext = os.path.splitext(input_path)
    return f"{root}_grouped.csv"

def main():
    ap = argparse.ArgumentParser(description="Group consecutive DP kernels; pass PP rows through.")
    ap.add_argument("input_csv", help="Path to input CSV")
    args = ap.parse_args()

    df = pd.read_csv(args.input_csv)
    cols_no_name = [c for c in df.columns if c != "Name"]
    if df.empty:
        out = pd.DataFrame(columns=cols_no_name + ["Start Name", "End Name"])
        out.to_csv(make_output_path(args.input_csv), index=False)
        print(f"Wrote grouped CSV: {make_output_path(args.input_csv)} (empty)")
        sys.exit(0)

    df["Start (ns)"] = df["Start (ns)"].apply(int)
    df["Duration (ns)"] = df["Duration (ns)"].apply(int)

    out_rows = []
    cur_group = None  # only used for DP groups

    for _, row in df.iterrows():
        p = row["Parallelism"]
        name = row["Name"]
        s = int(row["Start (ns)"])
        d = int(row["Duration (ns)"])

        if p == "DP":
            if cur_group is None:
                cur_group = {col: row[col] for col in cols_no_name}
                cur_group["Start (ns)"] = s
                cur_group["Duration (ns)"] = d
                cur_group["Start Name"] = name
                cur_group["End Name"] = name
            else:
                cur_group["Duration (ns)"] += d
                cur_group["End Name"] = name
        else:
            if cur_group is not None:
                out_rows.append(cur_group)
                cur_group = None
            passthrough = {col: row[col] for col in cols_no_name}
            passthrough["Start (ns)"] = s
            passthrough["Duration (ns)"] = d
            passthrough["Start Name"] = name
            passthrough["End Name"] = name
            out_rows.append(passthrough)

    if cur_group is not None:
        out_rows.append(cur_group)

    out_df = pd.DataFrame(out_rows, columns=cols_no_name + ["Start Name", "End Name"])
    out_df.to_csv(make_output_path(args.input_csv), index=False)
    print(f"Wrote grouped CSV: {make_output_path(args.input_csv)}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import os
import pandas as pd
import math

def group_consecutive_by_parallelism(df: pd.DataFrame) -> pd.DataFrame:
    # Coerce numeric columns
    df["Start (ns)"] = pd.to_numeric(df["Start (ns)"], errors="coerce")
    df["Duration (ns)"] = pd.to_numeric(df["Duration (ns)"], errors="coerce")
    if "Size(bytes)" in df.columns:
        df["Size(bytes)"] = pd.to_numeric(df["Size(bytes)"], errors="coerce")
    else:
        df["Size(bytes)"] = float("nan")

    # Drop rows missing essential timing
    df = df.dropna(subset=["Start (ns)", "Duration (ns)"]).copy()

    # Ensure sorted by Start (ns)
    df = df.sort_values("Start (ns)", kind="mergesort").reset_index(drop=True)
    starts = df["Start (ns)"].values
    assert all(starts[i] <= starts[i+1] for i in range(len(starts)-1)), \
        "Input must be sorted by Start (ns)."

    out_rows = []
    if df.empty:
        return pd.DataFrame(columns=[
            "Start (ns)", "End (ns)", "Duration (ns)",
            "Start Kernel Name", "End Kernel Name",
            "Total Size (bytes)", "Parallelism"
        ])

    # Initialize first group
    grp_start_idx = 0
    curr_par = str(df.loc[0, "Parallelism"])

    def flush_group(start_idx: int, end_idx_inclusive: int):
        """Summarize rows start_idx..end_idx_inclusive into one output row."""
        block = df.iloc[start_idx:end_idx_inclusive+1]
        start_ns = int(block.iloc[0]["Start (ns)"])
        last_start = int(block.iloc[-1]["Start (ns)"])
        last_dur = int(block.iloc[-1]["Duration (ns)"])
        end_ns = last_start + last_dur
        duration_ns = end_ns - start_ns

        start_name = str(block.iloc[0].get("Name", ""))
        end_name = str(block.iloc[-1].get("Name", ""))

        # Sum sizes, ignoring NaN
        sizes = pd.to_numeric(block["Size(bytes)"], errors="coerce")
        total_size = int(sizes.dropna().sum()) if not math.isnan(sizes.dropna().sum()) else 0

        out_rows.append({
            "Start (ns)": start_ns,
            "End (ns)": end_ns,
            "Duration (ns)": duration_ns,
            "Start Kernel Name": start_name,
            "End Kernel Name": end_name,
            "Total Size (bytes)": total_size,
            "Parallelism": str(block.iloc[0]["Parallelism"]),
        })

    # Walk rows and cut when Parallelism changes
    for i in range(1, len(df)):
        par = str(df.loc[i, "Parallelism"])
        if par != curr_par:
            flush_group(grp_start_idx, i-1)
            grp_start_idx = i
            curr_par = par

    # Flush last group
    flush_group(grp_start_idx, len(df)-1)

    return pd.DataFrame(out_rows)

def main():
    ap = argparse.ArgumentParser(
        description="Group consecutive kernels with the same Parallelism into summary rows."
    )
    ap.add_argument("csv", help="Input CSV path")
    ap.add_argument("-o", "--output", help="Output CSV (default: <input>_grouped.csv)")
    args = ap.parse_args()

    inp = args.csv
    out = args.output or os.path.splitext(inp)[0] + "_grouped.csv"

    df = pd.read_csv(inp)
    required = {"Start (ns)", "Duration (ns)", "Name", "Parallelism"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Missing required columns: {', '.join(sorted(missing))}")

    out_df = group_consecutive_by_parallelism(df)
    out_df.to_csv(out, index=False)
    print(f"Wrote {len(out_df)} grouped rows to {out}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(
        description="Separate events by rank (PID) and write per-PID CSVs in the same directory as the input."
    )
    parser.add_argument(
        "input_csv",
        help="Path to the input CSV file containing a 'PID' and 'Start (ns)' columns."
    )
    args = parser.parse_args()
    input_csv = args.input_csv

    # Determine output directory and base name
    input_path = os.path.abspath(input_csv)
    input_dir = os.path.dirname(input_path)
    base_name = os.path.splitext(os.path.basename(input_csv))[0]

    # Read the CSV
    df = pd.read_csv(input_csv)
    # Validate columns
    if "PID" not in df.columns:
        print("Error: 'PID' column not found in the input CSV.")
        return
    if "Start (ns)" not in df.columns:
        print("Error: 'Start (ns)' column not found in the input CSV.")
        return

    # Identify unique PIDs
    pids = sorted(df["PID"].unique())
    print(f"Found PIDs: {', '.join(str(pid) for pid in pids)}")
    if len(pids) != 4:
        print(f"Warning: Expected 4 unique PIDs but found {len(pids)}.")

    # For each PID, filter and write
    for pid in pids:
        df_pid = df[df["PID"] == pid].sort_values("Start (ns)")
        output_filename = f"{base_name}_pid_{pid}.csv"
        output_path = os.path.join(input_dir, output_filename)
        df_pid.to_csv(output_path, index=False)
        print(f"Wrote {len(df_pid)} rows for PID {pid} to {output_path}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import pandas as pd
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Filter a CUDA GPU trace CSV to only keep kernels whose Name starts with 'nccl'."
    )
    parser.add_argument(
        "input_csv",
        help="Path to the input CUDA GPU trace CSV (must have a 'Name' column)."
    )
    parser.add_argument(
        "output_csv",
        help="Path to write the filtered CSV."
    )
    args = parser.parse_args()

    # Load the CSV
    try:
        df = pd.read_csv(args.input_csv)
    except FileNotFoundError:
        print(f"Error: file not found: {args.input_csv}", file=sys.stderr)
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: no data: {args.input_csv}", file=sys.stderr)
        sys.exit(1)

    # Check for Name column
    if "Name" not in df.columns:
        print("Error: 'Name' column not found in input CSV.", file=sys.stderr)
        sys.exit(1)

    # Filter rows where Name starts with 'nccl'
    mask = df["Name"].astype(str).str.startswith("nccl")
    filtered = df[mask].copy()

    # Write out
    filtered.to_csv(args.output_csv, index=False)
    print(f"Wrote {len(filtered)} rows (kernels starting with 'nccl') to {args.output_csv}")

if __name__ == "__main__":
    main()

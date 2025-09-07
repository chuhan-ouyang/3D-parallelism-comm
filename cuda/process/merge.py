#!/usr/bin/env python3
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(
        description="Merge a CUDA GPU trace CSV and an NVTX trace CSV, "
                    "tag each row with its source, and sort by Start (ns)."
    )
    parser.add_argument(
        "cuda_csv",
        help="Path to the CUDA GPU trace CSV (with a 'Start (ns)' column)."
    )
    parser.add_argument(
        "nvtx_csv",
        help="Path to the NVTX trace CSV (with a 'Start (ns)' column)."
    )
    parser.add_argument(
        "output_csv",
        help="Path to write the merged, sorted CSV."
    )
    args = parser.parse_args()

    # Load both traces
    df_cuda = pd.read_csv(args.cuda_csv)
    df_nvtx = pd.read_csv(args.nvtx_csv)

    # Tag each row with its origin
    df_cuda["source"] = "cuda"
    df_nvtx["source"] = "nvtx"

    # Concatenate, keeping all columns
    merged = pd.concat([df_cuda, df_nvtx], ignore_index=True, sort=False)

    # Ensure we have the key column
    key = "Start (ns)"
    if key not in merged.columns:
        raise KeyError(f"Expected column '{key}' not found in inputs")

    # Sort by Start time and write out
    merged.sort_values(key, inplace=True)
    merged.to_csv(args.output_csv, index=False)

if __name__ == "__main__":
    main()

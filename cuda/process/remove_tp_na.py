#!/usr/bin/env python3
import argparse
import pandas as pd
import os

def main():
    parser = argparse.ArgumentParser(
        description="Keep only kernels with parallelism DP or PP"
    )
    parser.add_argument("input", help="Path to input CSV file")
    parser.add_argument(
        "-o", "--output",
        help="Path to output CSV file (default: <input>_dp_pp.csv)"
    )
    args = parser.parse_args()

    inp  = args.input
    out  = args.output or f"{os.path.splitext(inp)[0]}_dp_pp.csv"

    # load
    df = pd.read_csv(inp)

    # filter
    df2 = df[df['Parallelism'].isin(['DP', 'PP'])]

    # write back
    df2.to_csv(out, index=False)

if __name__ == "__main__":
    main()
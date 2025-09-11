#!/usr/bin/env python3
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(
        description="Count unique globalTid values in a CSV file"
    )
    parser.add_argument("input_csv", help="Path to the input CSV file")
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)

    if "globalTid" not in df.columns:
        raise SystemExit("Error: CSV does not contain a 'globalTid' column")

    counts = df["globalTid"].value_counts().sort_index()

    for tid, count in counts.items():
        print(f"{tid}: {count}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import csv
import os

def main():
    parser = argparse.ArgumentParser(
        description="Filter CSV rows where globalTid matches ncclTid or cclTid."
    )
    parser.add_argument("csv_path", help="Path to the input CSV file")
    parser.add_argument("ncclTid", help="globalTid value for NCCL rank 0")
    parser.add_argument("cclTid", help="globalTid value for CCL rank 0")
    args = parser.parse_args()

    input_csv = args.csv_path
    base, ext = os.path.splitext(input_csv)
    output_csv = f"{base}_rank0{ext}"

    keep_tids = {args.ncclTid, args.cclTid}

    kept = 0
    with open(input_csv, "r", newline="") as f_in, open(output_csv, "w", newline="") as f_out:
        reader = csv.DictReader(f_in)
        writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            if row.get("globalTid") in keep_tids:
                writer.writerow(row)
                kept += 1

    print(f"Filtered CSV written to {output_csv} ({kept} rows kept).")

if __name__ == "__main__":
    main()
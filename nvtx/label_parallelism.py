#!/usr/bin/env python3
import argparse
import csv
import json
import os

def normalize_comm_id(s: str) -> str:
    """Strip commas/spaces and return as plain string."""
    if s is None:
        return ""
    return "".join(ch for ch in str(s) if ch.isdigit())

def main():
    parser = argparse.ArgumentParser(
        description="Label rows with DP/TP/PP/NA based on NCCL communicator ID in jsonText."
    )
    parser.add_argument("csv_path", help="Path to the input CSV file")
    parser.add_argument("dp_comm", help="Data Parallel communicator ID (commas OK)")
    parser.add_argument("tp_comm", help="Tensor Parallel communicator ID (commas OK)")
    parser.add_argument("ppsend_comm", help="Pipeline Parallel SEND communicator ID (commas OK)")
    parser.add_argument("pprecv_comm", help="Pipeline Parallel RECV communicator ID (commas OK)")
    args = parser.parse_args()

    input_csv = args.csv_path
    base, ext = os.path.splitext(input_csv)
    output_csv = f"{base}_labeled{ext}"

    # Normalize the provided IDs (drop commas/spaces)
    dp_id = normalize_comm_id(args.dp_comm)
    tp_id = normalize_comm_id(args.tp_comm)
    pps_id = normalize_comm_id(args.ppsend_comm)
    ppr_id = normalize_comm_id(args.pprecv_comm)

    # For convenience, treat PP as union of send/recv IDs
    pp_ids = {pps_id, ppr_id}

    with open(input_csv, "r", newline="") as f_in, open(output_csv, "w", newline="") as f_out:
        reader = csv.DictReader(f_in)
        fieldnames = list(reader.fieldnames or [])
        if "Parallelism" not in fieldnames:
            fieldnames.append("Parallelism")

        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        total = 0

        for row in reader:
            total += 1
            parallelism = "NA"
            json_text = row.get("jsonText", "")

            if json_text:
                try:
                    payload = json.loads(json_text)
                    comm_id_raw = payload.get("NCCL communicator ID")
                    comm_id = normalize_comm_id(comm_id_raw)
                    if comm_id:
                        if comm_id == dp_id:
                            parallelism = "DP"
                        elif comm_id == tp_id:
                            parallelism = "TP"
                        elif comm_id in pp_ids:
                            parallelism = "PP"
                except Exception:
                    # Malformed JSON or unexpected structure -> leave as NA
                    pass

            row["Parallelism"] = parallelism
            writer.writerow(row)

    print(f"Wrote: {output_csv}")

if __name__ == "__main__":
    main()

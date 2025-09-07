#!/usr/bin/env python3
import argparse
import pandas as pd
import os
import json

def to_int(val):
    """Force to Python int to avoid NumPy overflow."""
    return int(val)

def main():
    nodes = [0, 1, 2, 3]

    base_dir = "/global/homes/c/co232/ReCCL-workspace/torchtitan/windows/nsys/cuda/traces"

    dfs = {}
    for node in nodes:
        path = os.path.join(base_dir, f"node{node}_cuda_gpu_trace_local_rank_0_filtered_labeled_dp_pp_synch_grouped.csv")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File not found: {path}")
        df = pd.read_csv(path)
        df["Start (ns)"] = df["Start (ns)"].apply(to_int)
        df["Duration (ns)"] = df["Duration (ns)"].apply(to_int)
        dfs[node] = df

    # PP circuits across all 4 nodes 
    pp_dfs = [dfs[node][dfs[node]["Parallelism"] == "PP"].reset_index(drop=True) for node in nodes]
    pp_counts = [len(df) for df in pp_dfs]
    assert all(c == 102 for c in pp_counts), f"Expected 102 PP kernels per rank, got counts: {pp_counts}"
    pp_len = 102

    pp_circuits = []
    for idx in range(pp_len):
        rows = [df.iloc[idx] for df in pp_dfs]
        print(f"PP circuit {idx}:")
        for node, row in zip(nodes, rows):
            start_val = to_int(row["Start (ns)"])
            end_val = start_val + to_int(row["Duration (ns)"])
            print(f"  Node {node}: start={start_val}, end={end_val}")

        start_ts = max(to_int(row["Start (ns)"]) for row in rows)
        end_ts   = max(to_int(row["Start (ns)"]) + to_int(row["Duration (ns)"]) for row in rows)
        pp_circuits.append({
            "Parallelism": "PP",
            "circuit_start_ts": start_ts,
            "circuit_end_ts": end_ts,
            "circuit_duration_ns": end_ts - start_ts,
            "circuit_nodes": json.dumps(nodes),
        })

    # DP circuits per pipeline stage (nodes[:2] and nodes[2:])
    dp_circuits = []
    for group in (nodes[:2], nodes[2:]):
        dp_dfs = [dfs[node][dfs[node]["Parallelism"] == "DP"].reset_index(drop=True) for node in group]
        dp_counts = [len(df) for df in dp_dfs]
        assert all(c == dp_counts[0] for c in dp_counts), f"DP kernel count mismatch in {group}: {dp_counts}"
        dp_len = dp_counts[0]
        print(f"DP Kernels Count for {group}: {dp_len}")

        for idx in range(dp_len):
            rows = [df.iloc[idx] for df in dp_dfs]

            print(f"DP circuit {idx} for group {group}:")
            for node, row in zip(group, rows):
                start_val = to_int(row["Start (ns)"])
                end_val = start_val + to_int(row["Duration (ns)"])
                print(f"  Node {node}: start={start_val}, end={end_val}")

            start_ts = max(to_int(row["Start (ns)"]) for row in rows)
            end_ts   = max(to_int(row["Start (ns)"]) + to_int(row["Duration (ns)"]) for row in rows)
            dp_circuits.append({
                "Parallelism": "DP",
                "circuit_start_ts": start_ts,
                "circuit_end_ts": end_ts,
                "circuit_duration_ns": end_ts - start_ts,
                "circuit_nodes": json.dumps(group),
            })

    all_circuits = pd.DataFrame(pp_circuits + dp_circuits).sort_values("circuit_end_ts").reset_index(drop=True)

    out_name = "rail0_circuit.csv"
    out_path = os.path.join(base_dir, out_name)
    all_circuits.to_csv(out_path, index=False)
    print(f"Global circuit windows written to {out_path}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(
        description="Calculate DP↔PP switch windows from labeled NCCL trace"
    )
    parser.add_argument(
        'input_csv',
        help='Path to the input CSV with a "Parallelism" column'
    )
    parser.add_argument(
        'output_csv',
        help='Path to write the computed windows CSV'
    )
    args = parser.parse_args()

    # Load the labeled trace
    df = pd.read_csv(args.input_csv)
    if df.empty:
        print("Input CSV is empty; no windows to compute.")
        return

    # # Force everything to Python ints to avoid any numpy overflow
    # df['Start (ns)']    = df['Start (ns)'].apply(int)
    # df['Duration (ns)'] = df['Duration (ns)'].apply(int)

    windows = []
    # Initialize with the first row
    prev_type = df.iloc[0]['Parallelism']
    prev_end = int(df.iloc[0]['Start (ns)']) + int(df.iloc[0]['Duration (ns)'])

    # Iterate over subsequent rows
    for _, row in df.iloc[1:].iterrows():
        curr_type = row['Parallelism']
        curr_start = int(row['Start (ns)'])
        curr_end = int(row['Start (ns)']) + int(row['Duration (ns)'])

        # Detect a switch in parallelism type
        if curr_type != prev_type:
            window_type = f"{prev_type}-{curr_type}"
            wind_start_ns = prev_end
            wind_end_ns = curr_start
            wind_duration_ns = wind_end_ns - wind_start_ns
            print(f"{wind_start_ns} - {wind_end_ns}")
            if wind_end_ns <= wind_start_ns:
                print(f"Warning: Overlapping window ({window_type})")
                wind_duration_ns = 0

            windows.append({
                'window_type': window_type,
                'wind_start_ns': wind_start_ns,
                'wind_end_ns': wind_end_ns,
                'wind_duration_ns': wind_duration_ns,
                'kernel_before_bytes': 0,
                'kernel_after_bytes': 0
            })

            # Update the previous type for next iteration
            prev_type = curr_type

        # Always update prev_end to the latest End (ns)
        prev_end = curr_end

    # Write out the windows
    out_df = pd.DataFrame(windows)
    out_df.to_csv(args.output_csv, index=False)
    print(f"Computed {len(windows)} switch windows and saved to {args.output_csv}")

if __name__ == '__main__':
    main()

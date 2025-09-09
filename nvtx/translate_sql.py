#!/usr/bin/env python3
import argparse
import sqlite3
import csv
import sys
from pathlib import Path

NVTX_COLS = [
    "start","end","eventType","rangeId","category","color","text",
    "globalTid","endGlobalTid","textId","domainId","uint64Value",
    "int64Value","doubleValue","uint32Value","int32Value","floatValue",
    "jsonTextId","jsonText","binaryData"
]

SELECT_SQL = """
SELECT
  e.start, e.end, e.eventType, e.rangeId, e.category, e.color, e.text,
  e.globalTid, e.endGlobalTid, e.textId, e.domainId, e.uint64Value,
  e.int64Value, e.doubleValue, e.uint32Value, e.int32Value, e.floatValue,
  e.jsonTextId, e.jsonText, e.binaryData,
  COALESCE(e.text, s.value) AS kernel_name
FROM NVTX_EVENTS e
LEFT JOIN StringIds s ON s.id = e.textId
ORDER BY e.end
"""

def parse_args():
    p = argparse.ArgumentParser(
        description="Export NVTX_EVENTS with kernel_name from a Nsight Systems SQLite DB."
    )
    p.add_argument("-i", "--input", required=True,
                   help="Path to input SQLite DB (e.g., 0_41047697_json.sqlite)")
    p.add_argument("-o", "--output", required=True,
                   help="Path to output CSV (e.g., nvtx_events_with_kernel_name.csv)")
    return p.parse_args()

def main():
    args = parse_args()
    db_path = Path(args.input)
    out_csv = Path(args.output)

    if not db_path.exists():
        print(f"Error: input DB not found: {db_path}", file=sys.stderr)
        sys.exit(1)

    con = sqlite3.connect(str(db_path))
    cur = con.cursor()

    # Count rows for a friendly message (optional)
    try:
        cur.execute("SELECT COUNT(*) FROM NVTX_EVENTS;")
        total = cur.fetchone()[0]
        print(f"Found {total} NVTX_EVENTS rows.")
    except sqlite3.OperationalError as e:
        print(f"Error reading NVTX_EVENTS: {e}", file=sys.stderr)
        con.close()
        sys.exit(1)

    # Fetch ALL rows (no batching as requested)
    cur.execute(SELECT_SQL)
    rows = cur.fetchall()

    header = NVTX_COLS + ["kernel_name"]
    with out_csv.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    con.close()

if __name__ == "__main__":
    main()

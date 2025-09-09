#!/usr/bin/env python3
#Reference: https://docs.nvidia.com/nsight-systems/2022.3/UserGuide/index.html#export-sqlite-examples

def decode_global_tid(globalTid: int):
    """Decode Nsight Systems globalTid into (PID, TID)."""
    PID = (globalTid // 0x1000000) % 0x1000000
    TID = globalTid % 0x1000000
    return PID, TID

def main():
    # Example globalTid values
    tids = [
        300180650918721,
        300180650919336
    ]

    for gtid in tids:
        pid, tid = decode_global_tid(gtid)
        print(f"globalTid={gtid} -> PID={pid}, TID={tid}")

if __name__ == "__main__":
    main()

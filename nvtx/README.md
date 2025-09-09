# NVTX Events Export and Processing

## Export NVTX Events from SQL
```bash
./run_translate_sql.sh # export a node's sqlite to csv with NCCL kernel names, times, and json info
```

## Filter for Rank 0
```bash
python decode_globalTID.py # decode globalTID to PID and TID to correspond globalTID to rank
```
* Node 0 Rank 0
globalTid=300180650918721 -> PID=1114945, TID=1114945
globalTid=300180650919336 -> PID=1114945, TID=1115560
* Node 1 Rank 0
    * NCCL globalTID: 
        * PID: 
        * TID: 
    * CCCL globalTID:
        * PID:
        * TID:
* Node 2 Rank 0
    * NCCL globalTID: 
        * PID: 
        * TID: 
    * CCCL globalTID:
        * PID:
        * TID: 
* Node 3 Rank 0
    * NCCL globalTID: 
        * PID: 
        * TID: 
    * CCCL globalTID:
        * PID:
        * TID: 
```bash
./run_filter_rank_0.sh # keep rank 0 data based on globalTID
```

## Label Parallelism
* Node 0 Rank 0
    * DP comm:
    * TP comm:
    * PPSend comm:
    * PPRecv comm:
* Node 1 Rank 0
    * DP comm:
    * TP comm:
    * PPSend comm:
    * PPRecv comm:
* Node 2 Rank 0
    * DP comm:
    * TP comm:
    * PPSend comm:
    * PPRecv comm:
* Node 3 Rank 0
    * DP comm:
    * TP comm:
    * PPSend comm:
    * PPRecv comm:
```bash
./run_label_parallelism.sh # label TP, DP, PP, NA
```
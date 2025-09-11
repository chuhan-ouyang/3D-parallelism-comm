# NVTX Events Export and Processing

## Export NVTX Events from SQL
```bash
./run_translate_sql.sh # export a node's sqlite to csv with NCCL kernel names, times, and json info
```

## Filter for Rank 0
```bash
python count_tids.py # print unique globalTID and counts
python decode_globalTID.py # decode globalTID to PID and TID to correspond globalTID to rank
```
* Node 0 Rank 0
PID: 1114945, TID: 1115560
globalTid=300180650918721 -> PID=1114945, TID=1114945
globalTid=300180650919336 -> PID=1114945, TID=1115560
* Node 1 Rank 0
PID: 964382, TID: 965434
globalTid=297662172543200 -> PID=964832, TID=964832
globalTid=297662172543802 -> PID=964832, TID=965434
* Node 2 Rank 0
PID: 563290, TID: 563881
globalTid=290925415274586 -> PID=563290, TID=563290
globalTid=290925415275177 -> PID=563290, TID=563881
* Node 3 Rank 0
PID: 951286, TID: 951876
globalTid=297434908361718 -> PID=951286, TID=951286
globalTid=297434908362308 -> PID=951286, TID=951876
```bash
./run_filter_rank_0.sh # keep rank 0 data based on globalTID
```

## Label Parallelism
* Node 0 Rank 0
    * DP comm: 3,574,919,951,526,054,331 
    * TP comm: 18,319,673,707,052,330,093 
    * PPSend comm: 6,004,158,948,986,910,404 
    * PPRecv comm: 6,831,535,697,949,778,466
* Node 1 Rank 0
    * DP comm: 3,574,919,951,526,054,331
    * TP comm: 454,674,816,390,077,854
    * PPSend comm: 2,194,994,131,262,233,267
    * PPRecv comm: 16,862,997,107,819,585,018
* Node 2 Rank 0
    * DP comm: 18,316,173,711,765,036,671
    * TP comm: 2,189,860,248,865,579,961
    * PPSend comm: 6,831,535,697,949,778,466
    * PPRecv comm: 6,004,158,948,986,910,404
* Node 3 Rank 0
    * DP comm: 18,316,173,711,765,036,671
    * TP comm: 17,041,003,602,900,097,456
    * PPSend comm: 16,862,997,107,819,585,018
    * PPRecv comm: 2,194,994,131,262,233,267
```bash
./run_label_parallelism.sh # label TP, DP, PP, NA
```
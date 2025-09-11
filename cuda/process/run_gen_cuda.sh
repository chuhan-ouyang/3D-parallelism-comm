#/bin/bash
# nsys stats \
#     --report=cuda_gpu_trace \
#     --format csv \
#     --output=../traces/node0 \
#     ../../nsys/0_41047697_json.sqlite

nsys stats \
    --report=cuda_gpu_trace \
    --format csv \
    --output=../traces/node1 \
    ../../nsys/1_41047697_json.sqlite

nsys stats \
    --report=cuda_gpu_trace \
    --format csv \
    --output=../traces/node2 \
    ../../nsys/2_41047697_json.sqlite

nsys stats \
    --report=cuda_gpu_trace \
    --format csv \
    --output=../traces/node3 \
    ../../nsys/3_41047697_json.sqlite
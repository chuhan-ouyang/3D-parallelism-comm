#/bin/bash
nsys stats \
    --report=cuda_gpu_trace \
    --format csv \
    --output=../traces/node0 \
    ../../nsys/0_41047697_json.sqlite

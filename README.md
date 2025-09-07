# 3D-parallelism-comm

## nsys
* nsys-rep traces and exported sqlite files
* export SQL with json NVTX payload:
```bash
nsys export --type=sqlite --include-json true --
output trace_with_json.sqlite <>.nsys-rep
```
* requires nsys version >= 2025.3

## nvtx
SQL extracted NVTX events

## cuda 
exported CUDA kernels

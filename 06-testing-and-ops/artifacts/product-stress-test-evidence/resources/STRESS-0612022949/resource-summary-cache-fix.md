# STRESS-0612022949 修复后资源摘要

## cache-fix-targeted

- 场景：`read_request_ladder` + `write_path`
- 样本数：150
- PostgreSQL 连接数：min 14 / max 49 / avg 46.49
- 容器峰值：
  - `server-postgres-1`：CPU 87.56%，内存 568.10 MiB
  - `server-rabbitmq-1`：CPU 67.28%，内存 193.70 MiB
  - `server-redis-1`：CPU 3.71%，内存 11.29 MiB
  - `server-minio-1`：CPU 13.23%，内存 112.30 MiB
  - `server-go-judge-1`：CPU 0.07%，内存 14.09 MiB

## cache-fix-soak

- 场景：`soak_stability`
- 样本数：84
- PostgreSQL 连接数：min 45 / max 49 / avg 48.14
- 容器峰值：
  - `server-postgres-1`：CPU 5.14%，内存 642.10 MiB
  - `server-rabbitmq-1`：CPU 64.13%，内存 210.30 MiB
  - `server-redis-1`：CPU 2.76%，内存 11.59 MiB
  - `server-minio-1`：CPU 11.96%，内存 121.00 MiB
  - `server-go-judge-1`：CPU 0.06%，内存 14.10 MiB

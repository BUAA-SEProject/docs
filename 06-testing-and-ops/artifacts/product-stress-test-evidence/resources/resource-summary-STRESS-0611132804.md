# STRESS-0611132804 资源采样摘要

- 资源原始样本：`product-stress-test-evidence/raw/STRESS-0611132804/contract-run/resource_samples.json`
- 样本数：358
- PostgreSQL 活跃连接峰值：49

| 容器 | CPU 峰值 | 内存峰值 |
| --- | ---: | ---: |
| `server-postgres-1` | 102.66% | 706.9 MiB |
| `server-redis-1` | 8.21% | 10.42 MiB |
| `server-rabbitmq-1` | 67.8% | 215.0 MiB |
| `server-minio-1` | 14.48% | 311.7 MiB |
| `server-go-judge-1` | 2.03% | 20.11 MiB |

## 瓶颈判断

高并发失败期间后端日志显示 Hikari 连接池耗尽：`total=48, active=48, idle=0, waiting=...`，与资源采样中的 PostgreSQL 活跃连接峰值 49 对齐。当前主要瓶颈不是 Redis、RabbitMQ、MinIO 或 go-judge 容器资源，而是应用端 JDBC 连接池/数据库访问路径在高并发读、通知轮询和判题轮询下的排队与超时。

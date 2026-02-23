# System Monitor Skill

## 描述
监控当前 OpenClaw 运行环境的系统状态，包括 CPU 负载、内存使用、Python/Node 进程数。
此能力用于诊断系统稳定性和高并发下的资源消耗情况。

## 文件
- `monitor.py`: 获取系统状态并输出 JSON。

## 用法
```bash
python3 /root/.openclaw/workspace/skills/system-monitor/monitor.py
```

## 输出示例
```json
{
  "timestamp": 1678886400.0,
  "platform": "Linux",
  "load_avg": [0.15, 0.10, 0.05],
  "cpu_count": 8,
  "memory": {
    "MemTotal": "16309872 kB",
    "MemFree": "8123456 kB",
    "MemAvailable": "12345678 kB"
  },
  "processes": {
    "python": 5,
    "node": 3
  }
}
```

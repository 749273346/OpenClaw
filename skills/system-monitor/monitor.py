import os
import sys
import json
import time
import subprocess

def get_system_status():
    status = {
        "timestamp": time.time(),
        "platform": os.uname().sysname if hasattr(os, 'uname') else sys.platform,
        "load_avg": os.getloadavg() if hasattr(os, 'getloadavg') else [],
        "cpu_count": os.cpu_count(),
    }
    
    # Memory
    try:
        if os.path.exists('/proc/meminfo'):
            meminfo = {}
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    parts = line.split(':')
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        if key in ['MemTotal', 'MemFree', 'MemAvailable']:
                            meminfo[key] = value
            status['memory'] = meminfo
    except Exception as e:
        status['memory'] = {"error": str(e)}

    # Process count (specifically python and node)
    try:
        python_procs = subprocess.run(['pgrep', '-c', 'python'], capture_output=True, text=True)
        node_procs = subprocess.run(['pgrep', '-c', 'node'], capture_output=True, text=True)
        status['processes'] = {
            'python': int(python_procs.stdout.strip()) if python_procs.stdout.strip() else 0,
            'node': int(node_procs.stdout.strip()) if node_procs.stdout.strip() else 0
        }
    except Exception as e:
        status['processes'] = {"error": str(e)}

    return status

if __name__ == "__main__":
    print(json.dumps(get_system_status(), indent=2))

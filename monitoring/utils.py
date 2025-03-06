# monitoring/utils.py
import psutil

def get_system_metrics():
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    return {
        'cpu_usage': cpu_usage,
        'memory_total': memory.total,
        'memory_used': memory.used,
        'memory_free': memory.free
    }


def get_process_info():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:10]  # Top 10 procesos


def get_network_info():
    network = psutil.net_io_counters()
    return {
        'bytes_sent': network.bytes_sent,
        'bytes_recv': network.bytes_recv,
        'packets_sent': network.packets_sent,
        'packets_recv': network.packets_recv
    }

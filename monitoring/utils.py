# monitoring/utils.py

import psutil
import time
import os
import platform
from datetime import datetime

def get_system_metrics():
    """Obtiene métricas avanzadas del sistema."""
    # CPU
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    
    # Intentar obtener temperatura de CPU (puede no estar disponible en todos los sistemas)
    cpu_temp = None
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
        if temps:
            # Intentar encontrar la temperatura de la CPU en diferentes formatos según el sistema
            for name, entries in temps.items():
                if name.lower() in ['coretemp', 'k10temp', 'cpu_thermal']:
                    if entries:
                        cpu_temp = entries[0].current
                        break
    
    # Memoria
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    # Disco
    disk = psutil.disk_usage('/')
    
    return {
        'cpu_usage': cpu_usage,
        'cpu_freq': cpu_freq.current if cpu_freq else None,
        'cpu_temp': cpu_temp,
        'memory_total': memory.total,
        'memory_used': memory.used,
        'memory_free': memory.available,
        'memory_buffers': memory.buffers if hasattr(memory, 'buffers') else None,
        'memory_cached': memory.cached if hasattr(memory, 'cached') else None,
        'swap_total': swap.total,
        'swap_used': swap.used,
        'disk_total': disk.total,
        'disk_used': disk.used,
        'disk_free': disk.free,
        'disk_percent': disk.percent
    }

def get_network_info():
    """Obtiene información detallada de red."""
    # Obtener estadísticas de red
    net_io = psutil.net_io_counters()
    
    # Obtener velocidades de transferencia
    net_stats_1 = psutil.net_io_counters()
    time.sleep(1)
    net_stats_2 = psutil.net_io_counters()
    
    # Calcular velocidades (bytes/s)
    bytes_sent_speed = net_stats_2.bytes_sent - net_stats_1.bytes_sent
    bytes_recv_speed = net_stats_2.bytes_recv - net_stats_1.bytes_recv
    
    # Obtener información de interfaces
    interfaces = []
    net_if_addrs = psutil.net_if_addrs()
    net_if_stats = psutil.net_if_stats()
    
    for interface, addrs in net_if_addrs.items():
        if interface in net_if_stats:
            stats = net_if_stats[interface]
            ip_addresses = []
            for addr in addrs:
                if addr.family == psutil.AF_LINK:  # MAC address
                    mac = addr.address
                elif addr.family == 2:  # IPv4
                    ip_addresses.append(addr.address)
            
            interfaces.append({
                'name': interface,
                'mac': mac if 'mac' in locals() else None,
                'ip_addresses': ip_addresses,
                'is_up': stats.isup,
                'speed': stats.speed if stats.speed > 0 else None  # Mbps
            })
    
    return {
        'bytes_sent': net_io.bytes_sent,
        'bytes_recv': net_io.bytes_recv,
        'packets_sent': net_io.packets_sent,
        'packets_recv': net_io.packets_recv,
        'errin': net_io.errin,
        'errout': net_io.errout,
        'dropin': net_io.dropin,
        'dropout': net_io.dropout,
        'bytes_sent_speed': bytes_sent_speed,  # bytes/s
        'bytes_recv_speed': bytes_recv_speed,  # bytes/s
        'interfaces': interfaces
    }

# monitoring/utils.py - Versión optimizada de get_process_info()

# monitoring/utils.py - Versión corregida de get_process_info()

def get_process_info():
    """Obtiene información detallada de los procesos de manera optimizada."""
    # Primero recolectar todos los PIDs
    all_pids = psutil.pids()
    
    # Inicializar cpu_percent para todos los procesos sin bloqueo
    for pid in all_pids:
        try:
            p = psutil.Process(pid)
            # Llamar a cpu_percent una vez sin intervalo para inicializar
            p.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    # Pequeña pausa para permitir que psutil recolecte datos de CPU
    time.sleep(0.1)
    
    # Ahora recolectar toda la información
    processes = []
    for pid in all_pids:
        try:
            p = psutil.Process(pid)
            
            # Verificar si el proceso sigue existiendo antes de continuar
            if not p.is_running():
                continue
                
            # Obtener cpu_percent sin bloqueo (ya inicializado)
            try:
                cpu_percent = p.cpu_percent(interval=None)
                memory_percent = p.memory_percent()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
            
            # Obtener tiempo de creación de forma segura
            try:
                create_time = p.create_time()
                create_time_str = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S')
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, ValueError, OSError):
                create_time = 0
                create_time_str = "N/A"
            
            # Solo recopilar información detallada si el proceso usa CPU significativa o es reciente
            if cpu_percent > 0.1 or (time.time() - create_time < 300):  # Procesos con uso de CPU o creados en los últimos 5 minutos
                process_info = {
                    'pid': pid,
                    'name': p.name() if hasattr(p, 'name') else f"Process-{pid}",
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory_percent,
                    'status': "unknown",
                    'create_time': create_time_str
                }
                
                # Obtener status de forma segura
                try:
                    process_info['status'] = p.status()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass  # Ya tiene valor por defecto
                
                # Obtener username solo si es necesario (operación costosa)
                try:
                    process_info['username'] = p.username()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    process_info['username'] = 'N/A'
                
                # Obtener información de memoria de forma segura
                process_info['memory_info'] = {'rss': 0, 'vms': 0}  # Valor por defecto
                try:
                    if hasattr(p, 'memory_info'):
                        mem_info = p.memory_info()
                        process_info['memory_info'] = {'rss': mem_info.rss, 'vms': mem_info.vms}
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, AttributeError):
                    pass  # Mantener los valores por defecto
                
                # Solo intentar obtener IO si el proceso tiene permisos
                process_info['io_read_bytes'] = None
                process_info['io_write_bytes'] = None
                
                try:
                    if hasattr(os, 'getuid') and os.getuid() == 0:  # Solo para root en sistemas Unix
                        if hasattr(p, 'io_counters'):
                            io_counters = p.io_counters()
                            process_info['io_read_bytes'] = io_counters.read_bytes
                            process_info['io_write_bytes'] = io_counters.write_bytes
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, AttributeError):
                    pass  # Mantener los valores por defecto
                
                processes.append(process_info)
        except Exception as e:
            # Capturar cualquier otra excepción que pueda ocurrir
            continue
    
    # Ordenar procesos por uso de CPU (descendente)
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    
    # Limitar a los 100 procesos más relevantes para evitar sobrecarga
    return processes[:20]

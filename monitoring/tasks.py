# monitoring/tasks.py

from .models import SystemMetrics, NetworkMetrics, ProcessInfo, NetworkInterface
from .utils import get_system_metrics, get_network_info, get_process_info
import time
import threading

def collect_metrics():
    """Recopila métricas del sistema y las guarda en la base de datos."""
    while True:
        try:
            # Recopilar y guardar métricas del sistema
            metrics = get_system_metrics()
            system_metrics = SystemMetrics(
                cpu_usage=metrics['cpu_usage'],
                cpu_freq=metrics['cpu_freq'],
                cpu_temp=metrics['cpu_temp'],
                memory_total=metrics['memory_total'],
                memory_used=metrics['memory_used'],
                memory_free=metrics['memory_free'],
                memory_buffers=metrics['memory_buffers'],
                memory_cached=metrics['memory_cached'],
                swap_total=metrics['swap_total'],
                swap_used=metrics['swap_used'],
                disk_total=metrics['disk_total'],
                disk_used=metrics['disk_used'],
                disk_free=metrics['disk_free'],
                disk_percent=metrics['disk_percent']
            )
            system_metrics.save()
            
            # Recopilar y guardar métricas de red
            network = get_network_info()
            network_metrics = NetworkMetrics(
                bytes_sent=network['bytes_sent'],
                bytes_recv=network['bytes_recv'],
                packets_sent=network['packets_sent'],
                packets_recv=network['packets_recv'],
                errin=network['errin'],
                errout=network['errout'],
                dropin=network['dropin'],
                dropout=network['dropout'],
                bytes_sent_speed=network['bytes_sent_speed'],
                bytes_recv_speed=network['bytes_recv_speed']
            )
            network_metrics.save()
            
            # Guardar información de interfaces
            for interface in network['interfaces']:
                for ip in interface.get('ip_addresses', []):
                    NetworkInterface.objects.create(
                        network_metrics=network_metrics,
                        name=interface['name'],
                        mac=interface['mac'],
                        ip_address=ip,
                        is_up=interface['is_up'],
                        speed=interface['speed']
                    )
            
            # Guardar información de procesos (solo los top 10 para no sobrecargar la DB)
            processes = get_process_info()[:10]
            for proc in processes:
                ProcessInfo.objects.create(
                    pid=proc['pid'],
                    name=proc['name'],
                    username=proc.get('username'),
                    status=proc.get('status'),
                    cpu_percent=proc['cpu_percent'],
                    memory_percent=proc['memory_percent'],
                    memory_rss=proc['memory_info'].get('rss') if proc['memory_info'] else None,
                    memory_vms=proc['memory_info'].get('vms') if proc['memory_info'] else None,
                    create_time=proc.get('create_time'),
                    io_read_bytes=proc.get('io_read_bytes'),
                    io_write_bytes=proc.get('io_write_bytes')
                )
            
            # Esperar 60 segundos antes de la siguiente recopilación
            time.sleep(60)
        except Exception as e:
            print(f"Error al recopilar métricas: {e}")
            time.sleep(60)  # Si hay error, esperar antes de intentar de nuevo

def start_metrics_collection():
    """Inicia la recopilación de métricas en un hilo separado."""
    thread = threading.Thread(target=collect_metrics, daemon=True)
    thread.start()
    return thread

def clean_old_data():
    """Elimina datos más antiguos que una semana."""
    from django.utils import timezone
    import datetime
    
    # Calcular fecha límite (una semana atrás)
    one_week_ago = timezone.now() - datetime.timedelta(days=7)
    
    # Eliminar métricas antiguas
    SystemMetrics.objects.filter(timestamp__lt=one_week_ago).delete()
    NetworkMetrics.objects.filter(timestamp__lt=one_week_ago).delete()


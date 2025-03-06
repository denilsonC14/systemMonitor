from .models import SystemMetrics, NetworkMetrics
from .utils import get_system_metrics, get_network_info
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
                memory_total=metrics['memory_total'],
                memory_used=metrics['memory_used'],
                memory_free=metrics['memory_free']
            )
            system_metrics.save()
            
            # Recopilar y guardar métricas de red
            network = get_network_info()
            network_metrics = NetworkMetrics(
                bytes_sent=network['bytes_sent'],
                bytes_recv=network['bytes_recv'],
                packets_sent=network['packets_sent'],
                packets_recv=network['packets_recv']
            )
            network_metrics.save()
            
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


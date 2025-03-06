
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from .utils import get_network_info, get_process_info, get_system_metrics
from .models import NetworkMetrics, ProcessInfo, SystemMetrics

def test_metrics(request):
    # Obtener métricas actuales
    metrics = get_system_metrics()
    
    # Guardar en la base de datos
    new_metrics = SystemMetrics(
        cpu_usage=metrics['cpu_usage'],
        memory_total=metrics['memory_total'],
        memory_used=metrics['memory_used'],
        memory_free=metrics['memory_free']
    )
    new_metrics.save()
    
    # Renderizar con template
    return render(request, 'monitoring/test.html', {'metrics': metrics})

def network_metrics(request):
    network_info = get_network_info()
    
    # Guardar en la base de datos
    new_network = NetworkMetrics(
        bytes_sent=network_info['bytes_sent'],
        bytes_recv=network_info['bytes_recv'],
        packets_sent=network_info['packets_sent'],
        packets_recv=network_info['packets_recv']
    )
    new_network.save()
    
    return render(request, 'monitoring/network.html', {'network_info': network_info})

def process_list(request):
    processes = get_process_info()
    # guardar en la base de datos
    
    return render(request, 'monitoring/processes.html', {'processes': processes})

# monitoring/views.py
def dashboard(request):
    """Vista para el panel de control principal"""
    metrics = get_system_metrics()
    network_info = get_network_info()
    processes = get_process_info()[:5]  # Solo los 5 procesos más intensivos
    
    # Calcular estado de alertas
    cpu_status = 'normal'
    if metrics['cpu_usage'] >= settings.MONITORING_THRESHOLDS['cpu_critical']:
        cpu_status = 'critical'
    elif metrics['cpu_usage'] >= settings.MONITORING_THRESHOLDS['cpu_warning']:
        cpu_status = 'warning'
    
    memory_percent = (metrics['memory_used'] / metrics['memory_total']) * 100
    memory_status = 'normal'
    if memory_percent >= settings.MONITORING_THRESHOLDS['memory_critical']:
        memory_status = 'critical'
    elif memory_percent >= settings.MONITORING_THRESHOLDS['memory_warning']:
        memory_status = 'warning'
    
    context = {
        'metrics': metrics,
        'network_info': network_info,
        'top_processes': processes,
        'status': {
            'cpu': cpu_status,
            'memory': memory_status
        }
    }
    
    return render(request, 'monitoring/dashboard.html', context)



# monitoring/views.py
from django.http import JsonResponse
from django.conf import settings

def get_realtime_data(request):
    """Endpoint para obtener datos actualizados en tiempo real con umbrales"""
    metrics = get_system_metrics()
    network_info = get_network_info()
    
    # Añadir estado de alerta basado en umbrales
    cpu_status = 'normal'
    if metrics['cpu_usage'] >= settings.MONITORING_THRESHOLDS['cpu_critical']:
        cpu_status = 'critical'
    elif metrics['cpu_usage'] >= settings.MONITORING_THRESHOLDS['cpu_warning']:
        cpu_status = 'warning'
    
    memory_percent = (metrics['memory_used'] / metrics['memory_total']) * 100
    memory_status = 'normal'
    if memory_percent >= settings.MONITORING_THRESHOLDS['memory_critical']:
        memory_status = 'critical'
    elif memory_percent >= settings.MONITORING_THRESHOLDS['memory_warning']:
        memory_status = 'warning'
    
    return JsonResponse({
        'metrics': metrics,
        'network_info': network_info,
        'status': {
            'cpu': cpu_status,
            'memory': memory_status
        },
        'timestamp': timezone.now().strftime('%H:%M:%S')
    })

# monitoring/views.py
def get_processes_data(request):
    """Endpoint para obtener datos actualizados de procesos"""
    processes = get_process_info()  # Reutiliza tu función existente
    
    return JsonResponse({
        'processes': processes,
        'timestamp': timezone.now().strftime('%H:%M:%S')
    })

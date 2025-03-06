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

def dashboard(request):
    # Obtener los datos más recientes
    system_metrics = get_system_metrics()
    network_info = get_network_info()
    processes = get_process_info()
    
    # Obtener datos históricos para los gráficos
    cpu_history = SystemMetrics.objects.order_by('-timestamp')[:60]  # Últimas 60 entradas
    
    context = {
        'system_metrics': system_metrics,
        'network_info': network_info,
        'top_processes': processes[:5],  # Solo los 5 procesos principales
        'cpu_history': list(cpu_history.values('timestamp', 'cpu_usage')),
    }
    
    return render(request, 'monitoring/dashboard.html', context)

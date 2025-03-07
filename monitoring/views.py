
import math
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from .utils import get_network_info, get_process_info, get_system_metrics
from .models import NetworkMetrics, ProcessInfo, SystemMetrics
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import time
from io import BytesIO

from django.conf import settings


@login_required
def test_metrics(request):
    # Obtener métricas actuales
    metrics = get_system_metrics()
    
    # Guardar en la base de datos
    new_metrics = SystemMetrics(
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
    new_metrics.save()
    
    # Renderizar con template
    return render(request, 'monitoring/test.html', {'metrics': metrics})

@login_required
def network_metrics(request):
    network_info = get_network_info()
    
    # Guardar en la base de datos
    new_network = NetworkMetrics(
        bytes_sent=network_info['bytes_sent'],
        bytes_recv=network_info['bytes_recv'],
        packets_sent=network_info['packets_sent'],
        packets_recv=network_info['packets_recv'],
        errin=network_info['errin'],
        errout=network_info['errout'],
        dropin=network_info['dropin'],
        dropout=network_info['dropout'],
        bytes_sent_speed=network_info['bytes_sent_speed'],
        bytes_recv_speed=network_info['bytes_recv_speed']

    )
    new_network.save()
    
    return render(request, 'monitoring/network.html', {'network_info': network_info, 'interfaces': network_info['interfaces']})

@login_required
def process_list(request):
    processes = get_process_info()
    # guardar en la base de datos
    
    return render(request, 'monitoring/processes.html', {'processes': processes})

# monitoring/views.py
@login_required
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
    
    disk_status = 'normal'
    if metrics['disk_percent'] >= 90:
        disk_status = 'critical'
    elif metrics['disk_percent'] >= 75:
        disk_status = 'warning'
    
    context = {
        'metrics': metrics,
        'network_info': network_info,
        'top_processes': processes,
        'now': timezone.now(),
        'status': {
            'cpu': cpu_status,
            'memory': memory_status,
            'disk': disk_status
        }
    }
    
    return render(request, 'monitoring/dashboard.html', context)

@login_required
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
    
    disk_status = 'normal'
    if metrics['disk_percent'] >= 90:
        disk_status = 'critical'
    elif metrics['disk_percent'] >= 75:
        disk_status = 'warning'
    
    return JsonResponse({
        'metrics': metrics,
        'network_info': network_info,
        'status': {
            'cpu': cpu_status,
            'memory': memory_status,
            'disk': disk_status
        },
        'timestamp': timezone.now().strftime('%H:%M:%S')
    })

@login_required
def get_processes_data(request):
    """Endpoint para obtener datos actualizados de procesos"""
    processes = get_process_info()  # Reutiliza tu función existente
    
    return JsonResponse({
        'processes': processes,
        'timestamp': timezone.now().strftime('%H:%M:%S')
    })

@login_required
def disk_metrics(request):
    """Vista para mostrar métricas de disco duro"""
    metrics = get_system_metrics()
    
    context = {
        'disk_total': metrics['disk_total'],
        'disk_used': metrics['disk_used'],
        'disk_free': metrics['disk_free'],
        'disk_percent': metrics['disk_percent']
    }
    
    return render(request, 'monitoring/disk.html', context)

@login_required
def export_metrics_pdf(request):
    """Exporta las métricas actuales del sistema a un archivo PDF."""
    
    # Crear un buffer de bytes para el PDF
    buffer = BytesIO()
    
    # Crear el objeto PDF usando ReportLab
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Título del documento
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, height - 50, "Informe de Monitoreo del Sistema")
    
    # Fecha y hora
    p.setFont("Helvetica", 10)
    timestamp = time.strftime("%d/%m/%Y %H:%M:%S")
    p.drawRightString(width - 50, height - 70, f"Generado: {timestamp}")
    
    # Obtener datos actuales
    metrics = get_system_metrics()
    network_info = get_network_info()
    processes = get_process_info()[:5]  # Solo los 5 procesos más intensivos
    
    # Sección de CPU
    y_position = height - 100
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y_position, "Información de CPU")
    
    y_position -= 25
    p.setFont("Helvetica", 12)
    p.drawString(50, y_position, f"Uso de CPU: {metrics['cpu_usage']}%")
    
    if metrics.get('cpu_freq'):
        y_position -= 20
        p.drawString(50, y_position, f"Frecuencia: {int(metrics['cpu_freq'])} MHz")
    
    if metrics.get('cpu_temp'):
        y_position -= 20
        p.drawString(50, y_position, f"Temperatura: {metrics['cpu_temp']:.1f}°C")
    
    # Sección de Memoria
    y_position -= 40
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y_position, "Información de Memoria")
    
    y_position -= 25
    p.setFont("Helvetica", 12)
    memory_percent = (metrics['memory_used'] / metrics['memory_total'] * 100)
    p.drawString(50, y_position, f"Memoria Total: {format_bytes(metrics['memory_total'])}")
    
    y_position -= 20
    p.drawString(50, y_position, f"Memoria Usada: {format_bytes(metrics['memory_used'])} ({memory_percent:.1f}%)")
    
    y_position -= 20
    p.drawString(50, y_position, f"Memoria Libre: {format_bytes(metrics['memory_free'])}")
    
    # Sección de Disco
    if 'disk_total' in metrics and metrics['disk_total']:
        y_position -= 40
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y_position, "Información de Disco")
        
        y_position -= 25
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position, f"Espacio Total: {format_bytes(metrics['disk_total'])}")
        
        y_position -= 20
        p.drawString(50, y_position, f"Espacio Usado: {format_bytes(metrics['disk_used'])} ({metrics['disk_percent']}%)")
        
        y_position -= 20
        p.drawString(50, y_position, f"Espacio Libre: {format_bytes(metrics['disk_free'])}")
    
    # Sección de Red
    y_position -= 40
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y_position, "Información de Red")
    
    y_position -= 25
    p.setFont("Helvetica", 12)
    p.drawString(50, y_position, f"Bytes Enviados: {format_bytes(network_info['bytes_sent'])}")
    
    y_position -= 20
    p.drawString(50, y_position, f"Bytes Recibidos: {format_bytes(network_info['bytes_recv'])}")
    
    y_position -= 20
    p.drawString(50, y_position, f"Velocidad de Subida: {format_bytes(network_info['bytes_sent_speed'])}/s")
    
    y_position -= 20
    p.drawString(50, y_position, f"Velocidad de Bajada: {format_bytes(network_info['bytes_recv_speed'])}/s")
    
    # Tabla de procesos
    y_position -= 40
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y_position, "Procesos Principales")
    
    # Crear tabla de procesos
    data = [['PID', 'Nombre', 'CPU (%)', 'Memoria (%)']]
    for proc in processes:
        data.append([
            str(proc['pid']),
            proc['name'],
            f"{proc['cpu_percent']:.1f}%",
            f"{proc['memory_percent']:.2f}%"
        ])
    
    # Dibujar tabla
    y_position -= 30
    table = Table(data, colWidths=[50, 200, 70, 70])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    # Ajustar la posición de la tabla
    table.wrapOn(p, width - 100, 100)
    table.drawOn(p, 50, y_position - 20 * len(data))
    
    # Pie de página
    p.setFont("Helvetica-Oblique", 8)
    p.drawCentredString(width/2, 30, "Este informe fue generado automáticamente por el Sistema de Monitoreo.")
    
    # Guardar el PDF
    p.showPage()
    p.save()
    
    # Obtener el valor del buffer y crear la respuesta HTTP
    pdf = buffer.getvalue()
    buffer.close()
    
    # Crear respuesta HTTP con el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sistema_monitoreo_informe.pdf"'
    response.write(pdf)
    
    return response

def format_bytes(bytes_value):
    """Formatea bytes a una representación legible."""
    if bytes_value == 0:
        return "0 Bytes"
    
    k = 1024
    sizes = ["Bytes", "KB", "MB", "GB", "TB"]
    i = int(math.floor(math.log(bytes_value) / math.log(k)))
    
    return f"{bytes_value / (k ** i):.2f} {sizes[i]}"
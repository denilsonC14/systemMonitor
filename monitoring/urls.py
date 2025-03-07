from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Ruta principal ahora es el dashboard
    path('test-metrics/', views.test_metrics, name='test_metrics'),
    path('network/', views.network_metrics, name='network_metrics'),
    path('processes/', views.process_list, name='process_list'),
    path('disk/', views.disk_metrics, name='disk_metrics'), 
    path('api/realtime-data/', views.get_realtime_data, name='realtime_data'),
    path('api/processes-data/', views.get_processes_data, name='processes_data'),
    path('export-pdf/', views.export_metrics_pdf, name='export_pdf'),
]

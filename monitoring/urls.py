from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Ruta principal ahora es el dashboard
    path('test-metrics/', views.test_metrics, name='test_metrics'),
    path('network/', views.network_metrics, name='network_metrics'),
    path('processes/', views.process_list, name='process_list'),
    path('api/realtime-data/', views.get_realtime_data, name='realtime_data'),
    path('api/processes-data/', views.get_processes_data, name='processes_data'),
]

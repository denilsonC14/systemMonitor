from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Ruta principal ahora es el dashboard
    path('test-metrics/', views.test_metrics, name='test_metrics'),
    path('network/', views.network_metrics, name='network_metrics'),
    path('processes/', views.process_list, name='process_list'),
 
]

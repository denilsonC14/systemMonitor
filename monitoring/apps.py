from django.apps import AppConfig


class MonitoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoring'

    def ready(self):
        # Importar aquí para evitar problemas de importación circular
        from .tasks import start_metrics_collection
        
        # Solo iniciar en el proceso principal, no en procesos de trabajo
        import os
        if os.environ.get('RUN_MAIN', None) != 'true':
            start_metrics_collection()

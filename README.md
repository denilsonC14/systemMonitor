# Sistema de Monitoreo de Recursos

Un sistema de monitoreo de recursos del sistema basado en Django que permite visualizar en tiempo real el uso de CPU, memoria, red y procesos.

## Características

- Monitoreo en tiempo real de CPU y memoria
- Seguimiento del tráfico de red
- Lista de procesos activos con uso de recursos
- Alertas visuales cuando los recursos alcanzan niveles críticos
- Interfaz web intuitiva y responsiva
- Sistema de autenticación de usuarios
- Tema claro/oscuro

## Requisitos

- Python 3.8+
- Django 3.2+
- Sistema operativo Linux
- Bibliotecas: psutil, plotly

## Instalación

1. Clonar el repositorio:
git clone https://github.com/tu-usuario/system-monitor.git
cd system-monitor


2. Crear un entorno virtual:
python -m venv venv
source venv/bin/activate
3. Instalar dependencias:
pip install -r requirements.txt

4. Aplicar migraciones:
python manage.py migrate

5. Crear un superusuario:
python manage.py runserver


## Uso

1. Accede a http://localhost:8000/ en tu navegador
2. Inicia sesión con tu cuenta
3. Explora las diferentes secciones del sistema de monitoreo:
- Dashboard: Vista general de todos los recursos
- Métricas Básicas: Detalles de CPU y memoria
- Detalles de Red: Información sobre el tráfico de red
- Lista de Procesos: Procesos activos y su consumo de recursos
- administracion: si es un administrador

## Configuración

Puedes personalizar la configuración en `system_monitor/settings.py`:

- `MONITORING_THRESHOLDS`: Umbrales para alertas de recursos
- `SYSTEM_DATA_CACHE_TIMEOUT`: Tiempo de caché para datos del sistema

## Pruebas

Para ejecutar las pruebas:
realizadas mediante sonarqube

## Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo LICENSE para más detalles.



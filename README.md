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

# Manual de Usuario - Sistema de Monitoreo de Recursos

## Introducción

El Sistema de Monitoreo de Recursos es una herramienta web que te permite visualizar y controlar el uso de recursos de tu sistema en tiempo real. Con esta aplicación podrás monitorear el uso de CPU, memoria, red y procesos activos, recibiendo alertas cuando algún recurso alcance niveles críticos.

## Acceso al Sistema

1. Abre tu navegador web y accede a la URL del sistema (por defecto: http://localhost:8000/)
2. En la pantalla de inicio de sesión, ingresa tus credenciales:
   - Usuario: Tu nombre de usuario
   - Contraseña: Tu contraseña

3. Si no tienes una cuenta, haz clic en "Registrarse" y completa el formulario con:
   - Nombre de usuario
   - Correo electrónico
   - Contraseña (y confirmación)

## Dashboard Principal

El dashboard principal muestra una vista general de todos los recursos del sistema:

- **Panel de CPU**: Muestra el porcentaje de uso actual de la CPU con un indicador de color:
  - Verde: Uso normal
  - Amarillo: Uso elevado (advertencia)
  - Rojo: Uso crítico

- **Panel de Memoria**: Muestra el uso de memoria RAM, tanto en valores absolutos como en porcentaje.

- **Panel de Red**: Muestra los bytes enviados y recibidos por las interfaces de red.

- **Panel de Procesos**: Muestra los 5 procesos que más recursos están consumiendo.

Todos los paneles se actualizan automáticamente cada pocos segundos.

## Secciones Principales

### Métricas Básicas

Muestra información detallada sobre el uso de CPU y memoria, incluyendo:
- Porcentaje de uso de CPU
- Memoria total
- Memoria usada
- Memoria libre

### Detalles de Red

Proporciona información sobre el tráfico de red:
- Bytes enviados
- Bytes recibidos
- Paquetes enviados
- Paquetes recibidos

### Lista de Procesos

Muestra todos los procesos activos en el sistema con:
- ID del proceso (PID)
- Nombre del proceso
- Uso de CPU (%)
- Uso de memoria (%)

Puedes filtrar los procesos por:
- Todos los procesos
- Alto uso de CPU (>5%)
- Medio uso de CPU (1-5%)
- Bajo uso de CPU (<1%)

## Preferencias de Usuario

### Cambiar Tema

Puedes cambiar entre el tema claro y oscuro haciendo clic en el botón de tema en la esquina inferior derecha de la pantalla.

### Perfil de Usuario

Para acceder a tu perfil:
1. Haz clic en tu nombre de usuario en la esquina superior derecha
2. Selecciona "Mi Perfil"

En tu perfil puedes ver:
- Tu nombre de usuario
- Tu correo electrónico
- Tu rol en el sistema

### Cerrar Sesión

Para cerrar sesión:
1. Haz clic en tu nombre de usuario en la esquina superior derecha
2. Selecciona "Cerrar Sesión"

## Solución de Problemas

Si encuentras algún problema al usar el sistema:

1. **La página no se actualiza automáticamente**: Verifica tu conexión a internet y recarga la página.

2. **Datos incorrectos o incompletos**: Cierra sesión, vuelve a iniciar sesión y verifica nuevamente.

3. **Errores de autenticación**: Asegúrate de que tus credenciales sean correctas. Si olvidaste tu contraseña, contacta al administrador del sistema.

4. **Rendimiento lento**: Si el sistema se ejecuta lentamente, cierra otras aplicaciones que puedan estar consumiendo recursos.




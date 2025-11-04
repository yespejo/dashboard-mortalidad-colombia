# Guía de Despliegue en Render

## Dashboard de Mortalidad - Colombia 2019

Esta guía te ayudará a desplegar la aplicación web del Dashboard de Mortalidad en Render.

## Archivos de Configuración Incluidos

### 1. `requirements.txt`
Contiene todas las dependencias de Python necesarias:
- Flask==2.3.3
- pandas==2.0.3
- plotly==5.17.0
- numpy==1.24.3
- gunicorn==21.2.0

### 2. `render.yaml`
Archivo de configuración específico para Render que define:
- Tipo de servicio: Web
- Comando de construcción: `pip install -r requirements.txt`
- Comando de inicio: `gunicorn --bind 0.0.0.0:$PORT app:app`
- Variables de entorno predefinidas

### 3. `Procfile`
Archivo alternativo para especificar el comando de inicio:
```
web: gunicorn --bind 0.0.0.0:$PORT app:app
```

### 4. `.env.example`
Plantilla de variables de entorno necesarias para el proyecto.

## Pasos para Desplegar en Render

### Opción 1: Despliegue Automático con render.yaml

1. **Subir el código a GitHub**
   ```bash
   git add .
   git commit -m "Preparar para despliegue en Render"
   git push origin main
   ```

2. **Conectar con Render**
   - Ve a [render.com](https://render.com)
   - Crea una cuenta o inicia sesión
   - Haz clic en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub

3. **Configuración Automática**
   - Render detectará automáticamente el archivo `render.yaml`
   - La configuración se aplicará automáticamente
   - El despliegue comenzará automáticamente

### Opción 2: Configuración Manual

1. **Crear Web Service**
   - En Render, selecciona "New +" → "Web Service"
   - Conecta tu repositorio

2. **Configurar el Servicio**
   - **Name**: `pythonweb-dashboard`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

3. **Variables de Entorno**
   - `PYTHON_VERSION`: `3.9.18`
   - `FLASK_ENV`: `production`

4. **Desplegar**
   - Haz clic en "Create Web Service"
   - Espera a que termine el proceso de construcción

## Estructura de Archivos Requerida

```
PythonWeb/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias Python
├── render.yaml           # Configuración Render
├── Procfile              # Comando de inicio alternativo
├── .env.example          # Plantilla variables de entorno
├── .gitignore            # Archivos a ignorar en Git
├── README.md             # Documentación del proyecto
├── DEPLOYMENT.md         # Esta guía de despliegue
└── data/                 # Datos CSV
    ├── ListMuertes.csv
    ├── DiviPola.csv
    ├── CodMuerte.csv
    └── Grupos.csv
```

## Verificación del Despliegue

Una vez desplegado, tu aplicación estará disponible en una URL como:
`https://pythonweb-dashboard.onrender.com`

### Funcionalidades Disponibles:
- **Dashboard Principal**: Vista general con navegación
- **Mapa de Mortalidad**: Distribución por departamentos
- **Tendencia Mensual**: Gráfico de líneas temporal
- **Ciudades Violentas**: Top municipios con más homicidios
- **Ciudades Seguras**: Municipios con menor mortalidad
- **Principales Causas**: Tabla de causas de muerte
- **Análisis por Género**: Comparación hombre/mujer
- **Distribución por Edades**: Grupos etarios

## Solución de Problemas

### Error de Construcción
- Verifica que `requirements.txt` esté en la raíz del proyecto
- Asegúrate de que todas las dependencias tengan versiones específicas

### Error de Inicio
- Confirma que el archivo `app.py` esté en la raíz
- Verifica que la variable `PORT` esté configurada correctamente

### Datos No Cargan
- Asegúrate de que la carpeta `data/` y todos los archivos CSV estén incluidos
- Verifica que los nombres de archivos coincidan exactamente

## Configuración de Producción

La aplicación está configurada para:
- **Debug Mode**: Deshabilitado en producción
- **Host**: `0.0.0.0` (acepta conexiones externas)
- **Puerto**: Variable de entorno `$PORT` (asignado por Render)
- **Servidor**: Gunicorn (servidor WSGI para producción)

## Monitoreo

Render proporciona:
- Logs en tiempo real
- Métricas de rendimiento
- Reinicio automático en caso de fallos
- SSL/HTTPS automático

## Costos

- **Plan Gratuito**: Incluido en la configuración
- **Limitaciones**: 
  - 750 horas/mes
  - Suspensión después de 15 minutos de inactividad
  - Tiempo de arranque en frío

Para uso en producción intensivo, considera actualizar a un plan de pago.

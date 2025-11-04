# Guía de Despliegue en Railway

## Dashboard de Mortalidad - Colombia 2019

Esta guía te ayudará a desplegar la aplicación web del Dashboard de Mortalidad en Railway.

## Archivos de Configuración para Railway

### 1. `railway.json`
Archivo de configuración principal para Railway:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn --bind 0.0.0.0:$PORT app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 2. `nixpacks.toml`
Configuración específica para Nixpacks (sistema de build de Railway):
```toml
[phases.setup]
nixPkgs = ['python39']

[phases.install]
cmds = ['pip install -r requirements.txt']

[phases.build]
cmds = ['echo "Build phase completed"']

[start]
cmd = 'gunicorn --bind 0.0.0.0:$PORT app:app'
```

### 3. `requirements.txt`
Dependencias de Python (sin cambios):
- Flask==2.3.3
- pandas==2.0.3
- plotly==5.17.0
- numpy==1.24.3
- gunicorn==21.2.0

### 4. `.env.example`
Variables de entorno actualizadas para Railway:
```env
# Configuración de Flask
FLASK_ENV=production
PORT=5000

# Configuración de Python
PYTHON_VERSION=3.9.18

# Variables específicas para Railway
RAILWAY_ENVIRONMENT=production
NIXPACKS_PYTHON_VERSION=3.9
```

## Pasos para Desplegar en Railway

### Método 1: Despliegue desde GitHub (Recomendado)

1. **Preparar el repositorio**
   ```bash
   git add .
   git commit -m "Configurar para despliegue en Railway"
   git push origin main
   ```

2. **Crear proyecto en Railway**
   - Ve a [railway.app](https://railway.app)
   - Crea una cuenta o inicia sesión
   - Haz clic en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Conecta tu repositorio de GitHub
   - Selecciona el repositorio del proyecto

3. **Configuración automática**
   - Railway detectará automáticamente los archivos de configuración
   - El build comenzará automáticamente usando Nixpacks
   - La aplicación se desplegará con la configuración definida

### Método 2: Despliegue con Railway CLI

1. **Instalar Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Autenticarse**
   ```bash
   railway login
   ```

3. **Inicializar proyecto**
   ```bash
   cd PythonWeb
   railway init
   ```

4. **Desplegar**
   ```bash
   railway up
   ```

### Método 3: Configuración Manual

1. **Crear nuevo proyecto**
   - En Railway, selecciona "New Project"
   - Elige "Empty Project"

2. **Conectar repositorio**
   - Ve a Settings → Source
   - Conecta tu repositorio de GitHub
   - Selecciona la rama principal

3. **Variables de entorno (opcional)**
   - Ve a Variables
   - Agrega las variables necesarias:
     - `RAILWAY_ENVIRONMENT=production`
     - `NIXPACKS_PYTHON_VERSION=3.9`

## Estructura de Archivos para Railway

```
PythonWeb/
├── app.py                    # Aplicación principal Flask
├── requirements.txt          # Dependencias Python
├── railway.json             # Configuración Railway
├── nixpacks.toml            # Configuración Nixpacks
├── Procfile                 # Comando de inicio (backup)
├── .env.example             # Variables de entorno
├── .gitignore               # Archivos a ignorar
├── README.md                # Documentación del proyecto
├── RAILWAY_DEPLOYMENT.md    # Esta guía
├── render.yaml              # Configuración Render (legacy)
└── data/                    # Datos CSV
    ├── ListMuertes.csv
    ├── DiviPola.csv
    ├── CodMuerte.csv
    └── Grupos.csv
```

## Características de Railway

### Ventajas sobre otras plataformas:
- **Build automático**: Detección automática de tecnologías
- **Escalado automático**: Ajuste automático de recursos
- **SSL gratuito**: HTTPS automático
- **Dominios personalizados**: Soporte para dominios propios
- **Base de datos integrada**: PostgreSQL, MySQL, Redis disponibles
- **Logs en tiempo real**: Monitoreo completo
- **Git-based deployment**: Despliegue automático con cada push

### Configuración de producción:
- **Python**: 3.9
- **Servidor**: Gunicorn
- **Host**: 0.0.0.0
- **Puerto**: Variable $PORT (asignado automáticamente)
- **Reinicio**: Automático en caso de fallos

## Verificación del Despliegue

Una vez desplegado, tu aplicación estará disponible en una URL como:
`https://pythonweb-dashboard-production.up.railway.app`

### Funcionalidades disponibles:
- **Dashboard Principal**: Vista general con navegación
- **Mapa de Mortalidad**: Distribución por departamentos
- **Tendencia Mensual**: Gráfico de líneas temporal
- **Ciudades Violentas**: Top municipios con más homicidios
- **Ciudades Seguras**: Municipios con menor mortalidad
- **Principales Causas**: Tabla de causas de muerte
- **Análisis por Género**: Comparación hombre/mujer
- **Distribución por Edades**: Grupos etarios

## Solución de Problemas

### Error de Build
```bash
# Verificar logs de build
railway logs --deployment
```

### Error de dependencias
- Asegúrate de que `requirements.txt` esté actualizado
- Verifica que todas las versiones sean compatibles

### Error de inicio
- Confirma que `railway.json` y `nixpacks.toml` estén configurados correctamente
- Verifica que el comando de inicio sea correcto

### Datos no cargan
- Asegúrate de que la carpeta `data/` esté incluida en el repositorio
- Verifica que los archivos CSV tengan los nombres correctos

## Monitoreo y Logs

### Ver logs en tiempo real:
```bash
railway logs
```

### Ver métricas:
- CPU y memoria en el dashboard de Railway
- Tiempo de respuesta
- Número de requests

### Configurar alertas:
- Railway puede enviar notificaciones por email
- Integración con Discord/Slack disponible

## Costos y Planes

### Plan Hobby (Gratuito):
- $5 USD de crédito mensual
- Ideal para proyectos personales
- Sin límite de tiempo de actividad

### Plan Pro:
- $20 USD/mes
- Recursos adicionales
- Soporte prioritario

### Ventajas sobre el plan gratuito de Render:
- No hay suspensión por inactividad
- Mejor rendimiento
- Más recursos incluidos

## Comandos Útiles de Railway CLI

```bash
# Ver estado del proyecto
railway status

# Ver variables de entorno
railway variables

# Abrir la aplicación en el navegador
railway open

# Ver logs
railway logs

# Conectar a la base de datos (si aplica)
railway connect

# Ejecutar comandos en el contenedor
railway run python manage.py migrate
```

## Migración desde Render

Si vienes de Render, los cambios principales son:

1. **Archivos nuevos**: `railway.json` y `nixpacks.toml`
2. **Variables de entorno**: Agregar `RAILWAY_ENVIRONMENT`
3. **Configuración**: Railway usa Nixpacks en lugar de buildpacks
4. **Dominio**: Nueva URL de Railway

El código de la aplicación no requiere cambios adicionales.

## Próximos Pasos

1. **Dominio personalizado**: Configurar tu propio dominio
2. **Base de datos**: Agregar PostgreSQL si necesitas persistencia
3. **CI/CD**: Configurar pipelines de testing
4. **Monitoreo**: Integrar herramientas de APM
5. **Backup**: Configurar respaldos automáticos

## Soporte

- **Documentación**: [docs.railway.app](https://docs.railway.app)
- **Discord**: Comunidad activa de Railway
- **GitHub**: Issues y discusiones
- **Email**: Soporte directo para planes de pago

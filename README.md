# Dashboard de Mortalidad - Colombia 2019

Un dashboard interactivo desarrollado en Flask para el análisis de datos de mortalidad en Colombia durante el año 2019. Esta aplicación web proporciona visualizaciones detalladas y análisis estadísticos basados en datos oficiales de defunciones.

## 🚀 Características

- **Mapa de Mortalidad**: Distribución de muertes por departamento
- **Tendencia Mensual**: Análisis temporal de la mortalidad a lo largo del año
- **Análisis de Violencia**: Identificación de municipios con mayor número de homicidios
- **Ciudades Seguras**: Municipios con menor índice de mortalidad
- **Principales Causas**: Ranking de las causas de muerte más frecuentes
- **Análisis por Género**: Comparación de mortalidad entre hombres y mujeres
- **Distribución por Edades**: Patrones de mortalidad por grupos etarios

## 📊 Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Visualización**: Plotly.js
- **Análisis de Datos**: Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript
- **Datos**: CSV (archivos de datos oficiales)

## 📁 Estructura del Proyecto

```
PythonWeb/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Documentación del proyecto
├── .gitignore           # Archivos excluidos del control de versiones
└── data/                # Directorio de datos
    ├── ListMuertes.csv  # Datos principales de defunciones
    ├── DiviPola.csv     # Códigos geográficos (DANE)
    ├── CodMuerte.csv    # Códigos CIE-10 de causas de muerte
    └── Grupos.csv       # Definición de grupos etarios
```

## 🛠️ Instalación y Configuración

### Prerrequisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/dashboard-mortalidad-colombia.git
   cd dashboard-mortalidad-colombia
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

5. **Acceder al dashboard**
   Abrir el navegador web y visitar: `http://localhost:5000`

## 📈 Uso del Dashboard

### Página Principal
La página de inicio presenta un menú con todas las visualizaciones disponibles, cada una con una descripción de su funcionalidad.

### Navegación
- Cada visualización tiene su propia página dedicada
- Botón "Volver al Dashboard" en cada página para regresar al menú principal
- Estadísticas resumidas en cada visualización

### Visualizaciones Disponibles

1. **Mapa de Mortalidad** (`/mapa`)
   - Gráfico de barras por departamento
   - Total de defunciones por región

2. **Tendencia Mensual** (`/lineas`)
   - Gráfico de líneas temporal
   - Identificación de picos y valles estacionales

3. **Ciudades Violentas** (`/violencia`)
   - Top 10 municipios con más homicidios
   - Análisis de seguridad ciudadana

4. **Ciudades Seguras** (`/seguras`)
   - Gráfico circular de municipios seguros
   - Menor índice de mortalidad

5. **Principales Causas** (`/causas`)
   - Tabla con códigos CIE-10
   - Ranking de causas de muerte

6. **Análisis por Género** (`/genero`)
   - Gráfico de barras apiladas
   - Comparación hombre/mujer por departamento

7. **Distribución por Edades** (`/edades`)
   - Histograma por grupos etarios
   - Análisis del ciclo de vida

## 📊 Fuentes de Datos

Los datos utilizados provienen de fuentes oficiales colombianas:

- **ListMuertes.csv**: Registro principal de defunciones 2019
- **DiviPola.csv**: Códigos DANE de división político-administrativa
- **CodMuerte.csv**: Códigos internacionales CIE-10 de causas de muerte
- **Grupos.csv**: Definición de categorías etarias

## 🔧 Configuración Técnica

### Variables de Entorno
La aplicación utiliza configuración por defecto:
- **Host**: `0.0.0.0` (todas las interfaces)
- **Puerto**: `5000`
- **Debug**: `True` (solo para desarrollo)

### Dependencias Principales
```
Flask==2.3.3
pandas==2.1.1
plotly==5.17.0
numpy==1.25.2
```

## 🚀 Despliegue en Producción

Para desplegar en producción, considerar:

1. **Cambiar configuración de debug**
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

2. **Usar un servidor WSGI**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Configurar proxy reverso** (Nginx recomendado)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork del proyecto
2. Crear una rama para la nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de los cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Contacto

Para preguntas o sugerencias sobre el proyecto, puedes contactar a través de:

- **GitHub Issues**: Para reportar bugs o solicitar funcionalidades
- **Email**: [tu-email@ejemplo.com]

## 🙏 Agradecimientos

- Datos proporcionados por entidades oficiales colombianas
- Comunidad de desarrolladores de Flask y Plotly
- Contribuidores del proyecto

---

**Nota**: Este dashboard está diseñado con fines educativos y de análisis. Los datos presentados corresponden al año 2019 y deben ser interpretados en su contexto histórico y metodológico correspondiente.

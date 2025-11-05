# Usa una imagen estable y ligera de Python
FROM python:3.11-slim

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . /app

# Actualiza pip y herramientas de build
RUN pip install --upgrade pip setuptools wheel

# Instala dependencias
RUN pip install -r requirements.txt

# Expone el puerto (Render asigna $PORT automáticamente)
EXPOSE 10000

# Comando de arranque de Flask con Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
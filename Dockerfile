# Usa una imagen oficial de Python
FROM python:3.11-slim

# Crea el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expón el puerto que Railway asignará
ENV PORT=5000

# Comando para ejecutar tu app Flask
CMD gunicorn app:app --bind 0.0.0.0:5000
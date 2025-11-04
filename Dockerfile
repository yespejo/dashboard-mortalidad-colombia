FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Define puerto por defecto (Railway sobreescribe este valor)
ENV PORT=5000

CMD sh -c "gunicorn --bind 0.0.0.0:$PORT --timeout 600 app:app"
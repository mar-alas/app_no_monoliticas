FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear directorio para las claves si no existe
RUN mkdir -p .keys

# Exponemos el puerto que usará la aplicación
EXPOSE 5002

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
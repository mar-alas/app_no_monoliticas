FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear directorio para las claves si no existe
RUN mkdir -p .keys

# Hacer ejecutable el script de inicio
RUN chmod +x startup.sh

# Exponemos el puerto que usará la aplicación
EXPOSE 5002

# Comando para ejecutar la aplicación
CMD ["./startup.sh"]

# Comando para ejecutar la aplicación
# CMD ["python", "app.py"]
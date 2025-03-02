# Usar una imagen base oficial de Python
FROM python:3.9-slim

# Crear directorio de trabajo
WORKDIR /src

# Copiar y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY src/ .

# Exponer el puerto de la app
EXPOSE 3001

# Comando de inicio
CMD ["python", "main.py"]

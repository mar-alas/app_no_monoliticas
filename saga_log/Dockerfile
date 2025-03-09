FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code - explicitly list all files to ensure they are copied
COPY app.py .
COPY config.py .
COPY consumidores.py .
COPY dto.py .
COPY eventos.py .
COPY servicios.py .

# Expose port
EXPOSE 5003

# Set environment variable
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Command to verify files exist before starting
RUN ls -la /app

# Run the application
CMD ["python", "app.py"]
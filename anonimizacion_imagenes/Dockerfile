#build with docker build -t anonimizacion_imagenes_image .
#run with docker run --rm --name anonimizacion_imagenes_container -p 5001:5001 anonimizacion_imagenes_image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 5001

# Command to run the application
#CMD ["python", "main.py"]
CMD [ "flask", "run", "--host=0.0.0.0" ]
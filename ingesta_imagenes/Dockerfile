# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade --no-cache-dir "pip<24.1" setuptools wheel
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

EXPOSE 5000
# Run the application
CMD ["python", "src/main.py"]
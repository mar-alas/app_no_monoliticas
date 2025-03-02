# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY src /app/src
COPY requirements.txt /app
# COPY .keys /app/.keys

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade --no-cache-dir "pip<24.1" setuptools wheel
RUN pip install -r requirements.txt

EXPOSE 5000

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Run the application
CMD ["python", "src/api/api.py"]
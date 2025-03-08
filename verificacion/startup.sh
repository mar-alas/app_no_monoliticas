#!/bin/bash

# Script de inicialización para el microservicio de verificación

echo "Iniciando microservicio de verificación..."

# Crear directorios necesarios
echo "Creando directorios de configuración..."
mkdir -p .keys

# Crear archivo key.json dummy si no existe (solo para pruebas)
if [ ! -f .keys/key.json ]; then
    echo "Creando archivo key.json dummy para pruebas..."
    echo '{"type": "service_account"}' > .keys/key.json
fi

# Verificar conexión a la base de datos
echo "Verificando conexión a la base de datos..."
python -c "
import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text

try:
    DB_USERNAME = os.getenv('DB_USERNAME', 'user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_HOSTNAME = os.getenv('DB_HOSTNAME', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    
    uri = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/verificacion_db'
    print(f'Conectando a {uri}')
    
    engine = create_engine(uri)
    with engine.connect() as connection:
        result = connection.execute(text('SELECT 1'))
        print('✅ Conexión a la base de datos exitosa')
except Exception as e:
    print(f'❌ Error al conectar a la base de datos: {str(e)}')
    # No fallamos aquí, ya que la base de datos podría tardar en iniciar
"

# Verificar conexión al broker
echo "Verificando conexión al broker..."
python -c "
import os
import pulsar
import time

try:
    broker_host = os.getenv('BROKER_HOST', 'localhost')
    broker_url = f'pulsar://{broker_host}:6650'
    print(f'Conectando al broker en: {broker_url}')
    
    # Intentar varias veces, ya que el broker puede tardar en iniciar
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            client = pulsar.Client(broker_url)
            # Solo para verificar la conexión
            producer = client.create_producer('test-topic')
            producer.close()
            client.close()
            print('✅ Conexión al broker exitosa')
            break
        except Exception as e:
            if attempt < max_attempts - 1:
                print(f'Intento {attempt+1} fallido, reintentando en 5 segundos...')
                time.sleep(5)
            else:
                raise e
except Exception as e:
    print(f'❌ Error al conectar al broker: {str(e)}')
    # No fallamos aquí, ya que el broker podría tardar en iniciar
"

# Iniciar la aplicación
echo "Iniciando el servicio..."
exec python app.py
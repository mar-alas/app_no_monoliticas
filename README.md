# app_no_monoliticas
Curso diseño de aplicaciones no monolíticas

## Instrucciones

### 1. Configuración del repositorio

Asegúrese de tener esto en el repositorio con `sudo`:

```bash
mkdir -p ./data/zookeeper
chmod -R 777 ./data/zookeeper
mkdir -p ./data/bookkeeper
chmod -R 777 ./data/bookkeeper
```

### 2. Ejecutar contenedores Microservicio Autenticación y Pulsar

Ejecute `docker-compose up` para correr todos los contenedores de Pulsar y el contenedor de el microservicio de Autenticación.

### 3. Iniciar la aplicación del microservicio de anonimización de imagenes

En la raiz del microservicio inicie la ejecución de `app.py`. Use un ambiente virtual. Si hay problemas instalando, use:

```bash
pip install --upgrade --no-cache-dir "pip<24.1" setuptools wheel
```

Si necesita actualizar el `PYTHONPATH` para correr desde la raíz del repositorio:

```bash
export PYTHONPATH=$(pwd)/anonimizacion_imagenes
```

Para instrucciones mas detalladas ver el README del microservicio.

### 4. Ver el mensaje del evento

Para ver el mensaje del evento, ejecute en su equipo (después de correr docker compose up):

```bash
docker exec -it broker bin/pulsar-client consume persistent://public/default/eventos-anonimizador -s my-subscription -n 0
```

```bash
docker exec -it broker bin/pulsar-client consume persistent://public/default/comando_ingesta_imagenes -s my-subscription -n 0
```

para listar los topicos:
```bash
docker exec -it broker bin/pulsar-admin topics list public/default
```


o con el siguiente comando adentro del contenedor del broker:

```bash
bin/pulsar-client consume persistent://public/default/eventos-anonimizador -s my-subscription -n 0
```
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

### 2. Ejecutar contenedores

Ejecute `docker-compose up` para correr todos los contenedores de Pulsar.

### 3. Iniciar la aplicación

Inicie la ejecución de `app.py`. Use un ambiente virtual. Si hay problemas instalando, use:

```bash
pip install --upgrade --no-cache-dir "pip<24.1" setuptools wheel
```

Si necesita actualizar el `PYTHONPATH` para correr desde la raíz del repositorio:

```bash
export PYTHONPATH=$(pwd)/anonimizacion_imagenes
```

### 4. Ver el mensaje del evento

Para ver el mensaje del evento, ejecute:

```bash
consume persistent://public/default/eventos-anonimizador -s my-subscription -n 0
```
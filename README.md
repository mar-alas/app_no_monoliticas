# Proyecto Saludtech de los alpes equipo Compumundohipermegared

Este es el repositorio donde desarrollamos nuestro proyecto del caso de estudio Saludtech de los alpes.

## Escenarios de Calidad a Probar

* Escenario #1 (Disponibilidad): Ante alta concurrencia de usuarios la ingesta de imágenes debe seguir operando normalmente.
* Escenario #4 (Escalabilidad): Crecer el sistema ante una carga de datos exponencial por parte de centros de salud y laboratorios.
* Escenario #8 (Seguridad): Los datos sin anonimizar solamente pueden ser accedidos por personas autorizadas.

## Decisiones sobre la arquitectura del proyecto

### Topologia administración de datos

Escogimos una topología de base de datos descentralizada. Cada microservicio tiene su base de datos independiente a los demás microservicios. Esta es la práctica ideal y en estos momentos no hay un costo importante de su implementación por es optamos por esta decisión. Es la práctica ideal debido a que las bases de datos de los microservicios quedan desacopladas entre si y gracias a esto los fallos en una base de datos no se van a propagar por fuera de su microservicio a las demás bases de datos.

### Tecnología de mensajería

Escogimos Avro como nuestra tecnología de serialización por su facil implementación con pulsar y debido a que es un esquema más rápido y robusto que JSON. El versionamiento de los mensajes de comandos o eventos lo hicimos en la carpeta de infraestructura de cada microservicio. Por ahora solamente estamos manejando la versión V1 que se puede ver en estas carpetas. 

### Actividades desarrolladas por cada integrante

* Daniel Gámez:
    * Desarrollo del microservición de anonimización de imagénes
    * Desarrollo Saga
* Maria del Mar Alas Escalante:
    * Desarrollo del microservición de ingesta de imagenes
* Jhon Puentes:
    * Desarrollo de los BFFs
* Robert Castro:
    * Desarrollo del microservicio de autenticacción
    * Despliegue en Kubernetes de la solución
    * Desarrollo de microservicio de verificación

## Estructura carpetas

```
.
├── README.md
├── docker-compose.yml: Archivo para correr microservicios en docker
├── Saludtech Microservicios.postman_collection.json: coleccion de postman
├── anonimizacion_imagenes: microservicio de anonimizacion de imagenes
├── ingesta_imagenes: microservicio de ingesta de imagenes
├── manejo_usuarios: microservicio de ingesta de gestión de usuario
├── repositorio_local: Imagenes de prueba en local
├── bff: Backend for Frontend
├── saga: Saga logs
├── verificador: microservicio de verificacion de anonimización

```
## Instrucciones

### 1. Configuración del repositorio

Asegúrese de tener en las carpetas "anonimizacion_imagenes" y "ingesta_imagenes" una subcarpeta ".keys" con el archivo de credenciales para GCP adentro. Este debe tener nombre "appnomonoliticas.json". Este archivo se descarga de GCP desde IAM.

### 2. Ejecutar contenedores Microservicio Autenticación y Pulsar

Ejecute `docker-compose up` para correr todos los contenedores de Pulsar, microservicio de Autenticación, microservicio anonimizacion y microservicio ingesta de imagenes.

### 3. Ver el mensaje del evento

Para ver los mensaje de los topicos, ejecute en su equipo (después de correr docker compose up):

```bash
docker exec -it broker bin/pulsar-client consume persistent://public/default/eventos-anonimizador -s my-subscription -n 0
```

```bash
docker exec -it broker bin/pulsar-client consume persistent://public/default/eventos-anonimizador-rollback -s my-subscription -n 0
```


```bash
docker exec -it broker bin/pulsar-client consume persistent://public/default/comando_anonimizacion_imagenes -s my-subscription -n 0
```

para listar los topicos:
```bash
docker exec -it broker bin/pulsar-admin topics list public/default
```
para borrar topicos:

```bash
docker exec -it broker bin/pulsar-admin topics delete public/default/eventos-anonimizador
```

para borrar mensajes en topicos con truncate:
```bash
docker exec -it broker bin/pulsar-admin topics truncate public/default/comando_ingestar_imagenes
```

bin/pulsar-admin namespaces get-backlog-size public/default

bin/pulsar-admin topics stats public/default/comando_ingestar_imagenes

bin/pulsar-admin namespaces set-retention public/default --size 300M --time 20m

con este se pueden borrar todos los topicos:
```bash
docker exec -it broker bash -c "for topic in eventos-bff comando_anonimizacion_imagenes_rollback comando_ingestar_imagenes eventos-fin-saga comando_anonimizacion_imagenes comando_ingestar_imagenes_rollback eventos-anonimizador eventos-ingesta-rollback eventos-ingesta eventos-verificacion; do bin/pulsar-admin topics delete persistent://public/default/\$topic; done"
```

```bash
docker exec -it broker bash -c "for topic in eventos-bff comando_anonimizacion_imagenes_rollback comando_ingestar_imagenes eventos-fin-saga comando_anonimizacion_imagenes comando_ingestar_imagenes_rollback eventos-anonimizador eventos-ingesta-rollback eventos-ingesta eventos-verificacion; do bin/pulsar-admin schemas delete persistent://public/default/\$topic; done"
```
o con el siguiente comando adentro del contenedor del broker:

```bash
bin/pulsar-client consume persistent://public/default/eventos-anonimizador -s my-subscription -n 0
```

con el siguiente comando se puede mandar un mensaje de prueba a un topico:
```bash
docker exec -it broker bin/pulsar-client produce persistent://public/default/comando_anonimizacion_imagenes_rollback -m "{hacer rollback}"
```

con el siguiente comando se puede conocer el esquema:
```bash
docker exec -it broker bin/pulsar-admin schemas get persistent://public/default/eventos-anonimizador
```

con el siguiente comando se puede borrar un topico:
```bash
docker exec -it broker bin/pulsar-admin topics delete persistent://public/default/eventos-anonimizador
```


## Para correr los microservicios en local:

sobre la raiz de anonimizacion:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

sobre la raiz de ingesta:

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python3 src/main.py
```

sobre la raiz de verificacion:

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python3 app.py
```


sobre la raiz de bff:

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python3 src/main.py
```


sobre la raiz de saga log:

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python3 app.py
```

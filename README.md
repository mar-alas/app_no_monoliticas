# Proyecto Saludtech de los alpes equipo Compumundohipermegared

Este es el repositorio donde desarrollamos nuestro proyecto del caso de estudio Saludtech de los alpes.

## Decisiones sobre la arquitectura del proyecto

### Topologia administración de datos

Escogimos una topología de base de datos descentralizada. Cada microservicio tiene su base de datos independiente a los demás microservicios. Esta es la práctica ideal y en estos momentos no hay un costo importante de su implementación por es optamos por esta decisión. Es la práctica ideal debido a que las bases de datos de los microservicios quedan desacopladas entre si y gracias a esto los fallos en una base de datos no se van a propagar por fuera de su microservicio a las demás bases de datos.

### Actividades desarrolladas por cada integrante

* Daniel Gámez:
    * Desarrollo del microservición de anonimización de imagénes
* Maria del Mar Alas Escalante:
    * Desarrollo del microservición de ingesta de imagenes de imagénes
* Jhon Puentes:
    * Desarrollo de los BFFs
* Robert Castro:
    * Desarrollo del microservicio de autenticacción
    * Despliegue en Kubernetes de la solución


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
docker exec -it broker bin/pulsar-client consume persistent://public/default/comando_anonimizacion_imagenes -s my-subscription -n 0
```

para listar los topicos:
```bash
docker exec -it broker bin/pulsar-admin topics list public/default
```


o con el siguiente comando adentro del contenedor del broker:

```bash
bin/pulsar-client consume persistent://public/default/eventos-anonimizador -s my-subscription -n 0
```

con el siguiente comando se puede mandar un mensaje de prueba a un topico:
```bash
docker exec -it broker bin/pulsar-client produce persistent://public/default/comando_anonimizacion_imagenes_rollback -m "{hacer rollback}
```
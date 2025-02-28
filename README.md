# app_no_monoliticas
Curso diseño de aplicaciones no monolíticas

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

con el siguiente comando se puede mandar un mensaje de prueba a un topico:
```bash
docker exec -it broker bin/pulsar-client produce persistent://public/default/comando_ingesta_imagenes_rollback -m "{hacer rollback}
```
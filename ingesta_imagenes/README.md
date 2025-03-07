## Estructura del Proyecto

Este proyecto utiliza una estructura modular organizada en varios componentes: `api`, `aplicacion`, `dominio`, `infraestructura`, y `seedwork`. A continuación se describe la estructura del árbol de directorios y la funcionalidad de cada componente:

```
.
├── README.md
└── src
    ├── api
    │   └── api.py
    ├── aplicacion
    │   ├── __init__.py
    │   ├── comandos
    │   │   ├── __init__.py
    │   │   └── crear_imagen_anonimizada.py
    │   ├── dto.py
    │   └── servicio_ingesta_imagen.py
    ├── dominio
    │   └── __init__.py
    ├── infraestructura
    │   ├── __init__.py
    │   ├── cola_comandos.py
    │   ├── gcp_storage.py
    │   └── schema
    │       └── v1
    │           └── comandos.py
    └── seedwork
        ├── README.md
        ├── aplicacion
        │   ├── __init__.py
        │   ├── autenticacion.py
        │   ├── comandos.py
        │   ├── dto.py
        │   └── handlers.py
        ├── dominio
        │   ├── __init__.py
        │   ├── eventos.py
        │   └── reglas.py
        └── infraestructura
            ├── __init__.py
            ├── schema
            │   └── v1
            │       ├── __init__.py
            │       ├── comandos.py
            │       └── mensajes.py
            └── utils.py
```

### Descripción de los Componentes

- **api**: Contiene el archivo `api.py` que expone una API REST para recibir una imagen. Esta imagen se pone en la cola de comandos para que otro microservicio (anonimizacion de imagenes) la procese y la guarde.

- **aplicacion**: 
  - **comandos**: Incluye el archivo `crear_imagen_anonimizada.py` que contiene el `IngestaImagenHandler`, el cual envía el comando con el objeto a la cola de comandos.
  - **dto.py**: Maneja el objeto que se va a enviar a la cola de comandos.
  - **servicio_ingesta_imagen.py**: Servicio principal para la ingesta de imágenes.

- **dominio**: Contiene la lógica de negocio y las reglas del dominio.

- **infraestructura**: 
  - **cola_comandos.py**: Maneja la cola de comandos.
  - **gcp_storage.py**: Interactúa con Google Cloud Storage.
  - **schema/v1/comandos.py**: Define los esquemas de los comandos.

- **seedwork**: 
  - **aplicacion**: Contiene componentes comunes como autenticación, manejo de comandos, DTOs y handlers.
  - **dominio**: Incluye eventos y reglas del dominio.
  - **infraestructura**: Contiene utilidades y esquemas comunes.

Esta estructura modular facilita la escalabilidad y el mantenimiento del proyecto, permitiendo una clara separación de responsabilidades y una mejor organización del código.

### Ejemplo de Publicación de Comando

El proyecto guarda la imagen en un bucket de GCP y envía un comando a un tópico de comandos que se vería así:

```
publishTime:[1740637658063], eventTime:[0], key:[null], properties:[], content:{"proveedor": "latam", "fecha_creacion": "2025-02-26T22:27:38.063302", "id": "4d17a605-e9d3-46be-883d-7418fce7ea50", "filename": "test_image.jpeg", "size": "161933", "binario_url": "https://storage.googleapis.com/imagenes-lat/4d17a605-e9d3-46be-883d-7418fce7ea50_test_image.jpeg", "mimetype": "image/jpeg"}
```

### Ejemplo de Request

El request se debe hacer a `http://127.0.0.1:5000/ingesta-imagen` agregando la imagen y el proveedor:

```sh
curl --location 'http://127.0.0.1:5000/ingesta-imagen' \
--header 'Authorization: ••••••' \
--form 'image=@"postman-cloud:///1eff4a48-3c7a-4d90-9662-ff05ca1d42a7"' \
--form 'proveedor="latam"'
```

### Ejemplo de Respuesta

La respuesta debería ser algo como:

```json
{
    "mensaje": "Imagen enviada para procesamiento"
}
```

### Información de Conexión a GCP

La información para conectarse a GCP está en `.key`.

### Pendiente

- TBD dejar el dockerfile funcionando y actualizar el docker-compose
- Por ahora activar el ambiente virtual de python3.10 instalar los requirements y correr src/api/api.py
- Ejecutar si hay problemas instalando los requiirements:
```sh
pip install --upgrade --no-cache-dir "pip<24.1" setuptools wheel
```

En caso de tener problemas por directorios correr el comando en linux:

```sh
 export PYTHONPATH=$PYTHONPATH:$(pwd)/src
```


```bash
docker exec -it ingesta_db psql -U user -d ingesta_db -c "\dt"
```


crear base de datos de prueba
```bash
docker exec -it ingesta_db psql -U user -d ingesta_db -c "SELECT * FROM ingesta_imagenes;"
```
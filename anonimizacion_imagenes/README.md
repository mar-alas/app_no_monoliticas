# Microservicio de Anonimización de Imágenes

## Descripción
Este microservicio se encarga de procesar y anonimizar imágenes, eliminando información sensible de textos encontrados en las imagenes. Para ver funcionamiento ver coleccion de postman encontrada en la carpeta del microservicio o ver las pruebas unitarias.


## Requisitos Técnicos
- Python 3.8+
- OpenCV
- Flask/FastAPI
- Docker

## Correr el contenedor de forma individual
1. Construir la imagen Docker:
```bash
docker build -t anonimizacion_imagenes_image .
```
2. Ejecutar el contenedor:
```bash
docker run --rm \
    --name anonimizacion_imagenes_container \
    --network app_no_monoliticas_pulsar \
    -p 5001:5001 \
    -e BROKER_HOST=broker \
    anonimizacion_imagenes_image
```
si desea probar la interaccion del componente con los demas puede correr en la raiz del repositorio este comando:

```bash
docker-compose --profile sin_anonimizacion up
```

## Correr el servicio en su ambiente local
Para ejecutar en modo desarrollo:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
o en Linux:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```
## Pruebas unitarias
Sobre la raiz del microservicio correr 

```bash
pytest
```




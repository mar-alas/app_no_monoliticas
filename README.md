# app_no_monoliticas
Curso diseño de aplicaciones no monoliticas

1. Asegurarse de tener esto en el repo con sudo:
mkdir -p ./data/zookeeper
chmod -R 777 ./data/zookeeper
mkdir -p ./data/bookkeeper
chmod -R 777 ./data/bookkeeper

2. Ejecutar docker-compose up para correr todos los contenedores de pulsar
3. Iniciar la ejecucion del app.py, usar un ambiente virtual, de haber problemas instalando usar:
pip install --upgrade --no-cache-dir "pip<24.1" setuptools wheel
Si necesita actualizar el PYTHONPATH para correr desde el root del repo:
export PYTHONPATH=$(pwd)/anonimizacion_imagenes

4. Para ver el mensaje del evento correr:
consume persistent://public/default/eventos-anonimizador -s my-subscription -n 0
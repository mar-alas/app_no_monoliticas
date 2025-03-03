```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```
o en Linux:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

En caso de tener problemas por directorios correr el comando en linux:

```sh
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
```
```sh
export ANONIMIZACION_SERVICE_URL=http://localhost:5001
```
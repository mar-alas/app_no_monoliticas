# BFF (Backend for Frontend) con Flask y Docker

Este proyecto implementa un Backend for Frontend (BFF) en Python usando Flask, con endpoints separados para web y mobile. 

## 📌 Estructura del Proyecto
```
📂 public-bff
 ├── 📂 src
 │   ├── 📂 api/v1
 │   │   ├── public_controller.py
 │   ├── 📂 services
 │   │   ├── ping_service.py
 │   ├── main.py
 ├── requirements.txt
 ├── venv
 ├── Dockerfile
 ├── readme.md
```

## Como hace parte de la arquitectura?
<img width="902" alt="image" src="https://github.com/user-attachments/assets/1af19c43-4e20-46a3-ad70-f5ddc6c792c1" />


## 🚀 Instalación y configuración

### 1️⃣ Clonar el repositorio
```bash
git clone <URL_DEL_REPO>
cd <NOMBRE_DEL_REPO>
```

### 2️⃣ Crear y activar un entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En macOS/Linux
venv\Scripts\activate    # En Windows
```

### 3️⃣ Instalar dependencias
```bash
pip install flask
pip freeze > requirements.txt
```

### 4️⃣ Ejecutar el servidor
```bash
python src/main.py
```

## 🐳 Usando Docker

### 1️⃣ Construir la imagen Docker
```bash
docker build -t public-bff .
```

### 2️⃣ Ejecutar el contenedor
```bash
docker run -p 3001:3001 public-bff
```

## 📡 Pruebas con cURL

### 🔹 Probar el servicio de ping
```bash
curl --request GET \
  --url http://localhost:3001/bff/public/v1/ping
```


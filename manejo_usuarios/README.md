# 🚀 Servicio de Manejo de Usuarios

Este servicio proporciona autenticación de usuarios con **Flask**, **PostgreSQL** y **JWT**, siguiendo principios de **Domain-Driven Design (DDD)**.

## 📂 Estructura del servicio

```plaintext
manejo_usuarios/
├── Dockerfile
├── README.md
├── app.py
├── pytest.ini
├── requirements.txt
├── src/
│   ├── api/                 # Endpoints de la API
│   ├── aplicacion/          # Lógica de negocio
│   ├── dominio/             # Entidades de dominio y repositorios
│   ├── infraestructura/     # Conexión con la base de datos
│   ├── seedwork/            # Código compartido
│   └── tests/               # Pruebas automatizadas
```

---

## ⚙️ Instalación y ejecución

### 🔹 1. Construir y levantar los contenedores

Ejecuta el siguiente comando:

```sh
docker compose up --build
```

Este comando hará lo siguiente:

- Construirá las imágenes de **Flask** y **PostgreSQL**.
- Creará la base de datos `user_db`.
- Expondrá el servicio en `http://localhost:8000`.

---

## 🔄 Reiniciar contenedores

Si necesitas limpiar los contenedores antes de reiniciar:

```sh
docker compose down -v
docker compose up --build
```

---

## 🚦 Pruebas de la API

### 1️⃣ Registrar un usuario

```sh
curl -X POST http://localhost:8000/auth/register \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Admin",
           "email": "admin@example.com",
           "password": "admin123"
         }'
```

### 2️⃣ Iniciar sesión y obtener token

```sh
curl -X POST http://localhost:8000/auth/login \
     -H "Content-Type: application/json" \
     -d '{
           "email": "admin@example.com",
           "password": "admin123"
         }'
```

**Respuesta esperada:**

```json
{
  "message": "Autenticación exitosa",
  "token": "eyJhbGciOiJIUzI1..."
}
```

### 3️⃣ Acceder a una ruta protegida (`/auth/profile`)

```sh
curl -X GET http://localhost:8000/auth/profile \
     -H "Authorization: Bearer TOKEN_AQUI"
```

Si el token es válido:

```json
{
  "message": "Perfil de usuario",
  "user_id": "d290f1ee-6c54-4b01-90e6-d701748f0851"
}
```

Si el token es inválido:

```json
{
  "message": "Token inválido o expirado"
}
```

---

## 📌 Base de datos

El servicio usa **PostgreSQL** y crea una base de datos llamada `user_db`. Puedes conectarte manualmente con:

```sh
docker exec -it user_db psql -U user -d user_db
```

Para verificar los usuarios creados:

```sql
SELECT * FROM users;
```

---

## 🛑 Detener y eliminar el servicio

```sh
docker compose down
```

Para eliminar todo, incluyendo volúmenes:

```sh
docker compose down -v
```


## 📌 Patrones y metodologías DDD aplicadas

### 📂 Patrones de diseño
- **Repository Pattern** → Implementado en `user_repository.py` y `sql_user_repository.py` para manejar la persistencia de usuarios.
- **Dependency Injection** → Se inyectan repositorios en los servicios de aplicación (`AuthenticationService`) para mejorar la modularidad.

### 📌 Metodologías DDD
- **Entidades** → `User` en `dominio/user.py` con identidad única y atributos relevantes.
- **Servicios de aplicación** → `AuthenticationService` y `TokenService` encapsulan la lógica de autenticación y generación de tokens.
- **Repositorios** → `UserRepository` en `dominio/user_repository.py` y su implementación en `infraestructura/sql_user_repository.py`.
- **Bounded Context** → `manejo_usuarios` como un microservicio aislado dentro del ecosistema.
- **Separation of Concerns** → División clara entre `dominio`, `aplicacion`, `infraestructura` y `api`, asegurando modularidad.

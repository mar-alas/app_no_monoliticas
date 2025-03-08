# Microservicio de Verificación de Anonimización

Este microservicio es responsable de verificar si las imágenes han sido correctamente anonimizadas. Recibe eventos del microservicio de anonimización, verifica la anonimización (con un algoritmo simulado 50/50) y emite eventos con el resultado.

## Estructura del proyecto

```
verificacion/
├── Dockerfile
├── README.md
├── app.py
├── requirements.txt
├── src/
│   ├── api/              # API REST
│   ├── aplicacion/       # Lógica de aplicación
│   ├── config/           # Configuración
│   ├── dominio/          # Entidades y reglas de dominio
│   ├── infraestructura/  # Componentes de infraestructura
│   └── seedwork/         # Componentes compartidos
├── startup.sh            # Script de inicio
└── tests/                # Pruebas
```

## Ejecutar

Ejecutar con Docker Compose:

```bash
docker-compose up -d verificacion_service
```

Ejecutar en local con:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

## Configuración

El microservicio utiliza las siguientes variables de entorno:

- `BROKER_HOST`: Host del broker Pulsar (default: "localhost")
- `DB_USERNAME`: Usuario de la base de datos (default: "user")
- `DB_PASSWORD`: Contraseña de la base de datos (default: "password") 
- `DB_HOSTNAME`: Host de la base de datos (default: "localhost")
- `DB_PORT`: Puerto de la base de datos (default: "9003")
- `PORT`: Puerto en el que se expondrá la API (default: 5002)

## API REST

### Endpoints Básicos

#### GET /verificacion/ping
Verifica que el servicio esté en ejecución.

**Respuesta**: `pong`

#### GET /verificacion/estado
Verifica el estado general del servicio.

**Respuesta**:
```json
{
  "servicio": "verificacion_anonimizacion",
  "estado": "activo",
  "version": "1.0.0",
  "base_datos": "conectada",
  "verificaciones_24h": 42,
  "timestamp": "2025-03-07T15:30:00.000Z"
}
```

### Endpoints de Verificaciones

#### GET /verificacion/todas
Obtiene todas las verificaciones con paginación.

**Parámetros**:
- `pagina`: Número de página (default: 1)
- `por_pagina`: Elementos por página (default: 10, max: 100)

**Respuesta**:
```json
{
  "data": [
    {
      "id": "uuid-verificacion",
      "id_imagen": "uuid-imagen",
      "nombre_imagen": "imagen.jpg",
      "resultado": "APROBADA",
      "detalle": "La imagen ha sido correctamente anonimizada",
      "fecha_verificacion": "2025-03-07T15:30:00.000Z",
      "proveedor": "lat"
    }
  ],
  "meta": {
    "pagina_actual": 1,
    "total_paginas": 5,
    "total_registros": 42,
    "por_pagina": 10
  }
}
```

#### GET /verificacion/{id_verificacion}
Obtiene detalles de una verificación específica.

**Respuesta**:
```json
{
  "id": "uuid-verificacion",
  "id_imagen": "uuid-imagen",
  "nombre_imagen": "imagen.jpg",
  "resultado": "APROBADA",
  "detalle": "La imagen ha sido correctamente anonimizada",
  "fecha_verificacion": "2025-03-07T15:30:00.000Z",
  "proveedor": "lat"
}
```

#### GET /verificacion/imagen/{id_imagen}
Obtiene todas las verificaciones para una imagen específica.

**Respuesta**: Lista de verificaciones en formato JSON.

#### GET /verificacion/estadisticas
Obtiene estadísticas sobre las verificaciones.

**Respuesta**:
```json
{
  "global": {
    "total": 100,
    "aprobadas": 65,
    "rechazadas": 35,
    "porcentaje_aprobadas": 65.0,
    "porcentaje_rechazadas": 35.0
  },
  "ultimo_dia": {
    "total": 10,
    "aprobadas": 6,
    "rechazadas": 4,
    "porcentaje_aprobadas": 60.0,
    "porcentaje_rechazadas": 40.0,
    "fecha_inicio": "2025-03-06T15:30:00.000Z"
  },
  "ultima_semana": {
    "total": 50,
    "aprobadas": 32,
    "rechazadas": 18,
    "porcentaje_aprobadas": 64.0,
    "porcentaje_rechazadas": 36.0,
    "fecha_inicio": "2025-02-28T15:30:00.000Z"
  },
  "ultimo_mes": {
    "total": 90,
    "aprobadas": 60,
    "rechazadas": 30,
    "porcentaje_aprobadas": 66.67,
    "porcentaje_rechazadas": 33.33,
    "fecha_inicio": "2025-02-07T15:30:00.000Z"
  },
  "timestamp": "2025-03-07T15:30:00.000Z"
}
```

#### POST /verificacion/solicitar
Solicita una verificación manual.

**Cuerpo de la solicitud**:
```json
{
  "id_imagen": "uuid-imagen",
  "filename": "imagen.jpg",
  "proveedor": "lat"
}
```

**Respuesta**:
```json
{
  "id_verificacion": "uuid-verificacion",
  "resultado": "APROBADA",
  "detalle": "La imagen ha sido correctamente anonimizada",
  "fecha_verificacion": "2025-03-07T15:30:00.000Z"
}
```

#### GET /verificacion/metricas
Obtiene métricas de rendimiento del servicio.

**Respuesta**:
```json
{
  "total_verificaciones": 100,
  "verificaciones_hoy": 10,
  "uptime": "3d 2h 15m",
  "memoria_usada": "128MB",
  "cpu_usada": "5%",
  "timestamp": "2025-03-07T15:30:00.000Z"
}
```

## Eventos

### Eventos consumidos

El microservicio se suscribe al tópico `eventos-anonimizador` para recibir eventos de imágenes anonimizadas.

**Formato del evento**:
```json
{
  "id": "uuid-evento",
  "time": 1709829000000,
  "data": {
    "id_imagen": "uuid-imagen",
    "filename": "imagen.jpg",
    "size": "1024",
    "fecha_creacion": "2025-03-07T15:30:00.000Z"
  }
}
```

### Eventos publicados

El microservicio publica eventos en el tópico `eventos-verificacion` con los resultados de la verificación.

**Formato del evento**:
```json
{
  "id": "uuid-evento",
  "time": 1709829000000,
  "specversion": "v1",
  "type": "VerificacionCompletada",
  "datacontenttype": "application/json",
  "service_name": "verificacion_anonimizacion",
  "data": {
    "id_verificacion": "uuid-verificacion",
    "id_imagen": "uuid-imagen",
    "filename": "imagen.jpg",
    "resultado": "APROBADA",
    "detalle": "La imagen ha sido correctamente anonimizada",
    "fecha_verificacion": "2025-03-07T15:30:00.000Z"
  }
}
```

## Pruebas

Para ejecutar las pruebas:

```bash
docker-compose run --rm verificacion_service python tests/test_flujo_completo.py
```

from fastapi import FastAPI, Request, BackgroundTasks, File, Form, UploadFile, Depends, HTTPException
import asyncio
import uvicorn
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseSettings
from typing import Any, List
from pulsar.schema import AvroSchema
from src.consumidores import suscribirse_a_topico
from src.api.v1.router import router as v1
from src.infraestructura.schema.v1.eventos import EventoIntegracionImagenAnonimizada
import requests
import os
from api.v1.ingestar import router as ingestar_imagen
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

class Config(BaseSettings):
    APP_VERSION: str = "1.0"
    ANONIMIZACION_SERVICE_URL: str = os.getenv("ANONIMIZACION_SERVICE_URL","http://localhost:5001")
    INGESTA_SERVICE_URL: str = os.getenv("INGESTA_SERVICE_URL", "http://localhost:5000")

settings = Config()
app_configs: dict[str, Any] = {"title": "BFF-Imagenes"}

app = FastAPI(**app_configs)
tasks = list()
eventos = list()
security = HTTPBearer()

@app.on_event("startup")
async def app_startup():
    global tasks
    global eventos
    # Suscripción a eventos de anonimización
    # task1 = asyncio.ensure_future(suscribirse_a_topico("eventos-anonimizador", "bff-subscription", AvroSchema(EventoIntegracionImagenAnonimizada), eventos=eventos))
    # tasks.append(task1)

@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()

@app.get('/bff/stream')
async def stream_mensajes(request: Request):
    def nuevo_evento():
        global eventos
        return {'data': eventos.pop(), 'event': 'NuevoEvento'}
    
    async def leer_eventos():
        global eventos
        while True:
            # Si el cliente cierra la conexión deja de enviar eventos
            if await request.is_disconnected():
                break

            if len(eventos) > 0:
                yield nuevo_evento()

            await asyncio.sleep(0.1)

    return EventSourceResponse(leer_eventos())

@app.get('/bff/ping')
async def ping():
    return {"status": "up"}

@app.post('/bff/login')
async def login(request: Request):
    try:
        # Get JSON body content
        body_json = await request.json()
        
        # Get authentication service URL from environment variable or use default
        USER_AUTH_SERVICE_URL = os.getenv("USER_AUTH_SERVICE_URL", "http://localhost:8000")
        
        # Forward the request to authentication service
        response = requests.post(
            f"{USER_AUTH_SERVICE_URL}/auth/login", 
            json=body_json,
            headers={"Content-Type": "application/json"}
        )
        
        # Return the authentication service response
        return response.json()
    except Exception as e:
        return {"error": str(e), "status_code": 500}

app.include_router(v1, prefix="/bff/v1")
app.include_router(ingestar_imagen, prefix="/bff/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
from fastapi import FastAPI, Request, BackgroundTasks
import asyncio
import uvicorn
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseSettings
from typing import Any, List

from src.consumidores import suscribirse_a_topico
from src.api.v1.router import router as v1

class Config(BaseSettings):
    APP_VERSION: str = "1.0"
    ANONIMIZACION_SERVICE_URL: str = "http://anonimizacion_service:5001"

settings = Config()
app_configs: dict[str, Any] = {"title": "BFF-Imagenes"}

app = FastAPI(**app_configs)
tasks = list()
eventos = list()

@app.on_event("startup")
async def app_startup():
    global tasks
    global eventos
    # Suscripción a eventos de anonimización
    task1 = asyncio.ensure_future(suscribirse_a_topico("eventos-anonimizador", "bff-subscription", "public/default/eventos-anonimizador", eventos=eventos))
    tasks.append(task1)

@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()

@app.get('/stream')
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

@app.get('/ping')
async def ping():
    return {"status": "up"}

# Router GraphQL
app.include_router(v1, prefix="/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
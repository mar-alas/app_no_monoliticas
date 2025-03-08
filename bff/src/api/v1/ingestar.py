import logging
import uuid
from fastapi import APIRouter, Request, UploadFile, Form, File, Response, Depends
from src.seedwork.aplicacion.autenticacion import token_required
from strawberry.fastapi.context import BaseContext
from .mutaciones import Mutation
import strawberry
from .consultas import Query
from io import BytesIO
import base64
from src.despachadores import Despachador
from src.infraestructura.schema.v1.eventos import InicioSagaPayload,EventoIntegracionInicioSaga
from pulsar.schema import AvroSchema

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/ingesta-imagen")
async def ingestar_imagen(
    request: Request,
    image: UploadFile = File(...),
    proveedor: str = Form(...),
    current_user: str = Depends(token_required)  # Use the token_required dependency
):
    
    logger.info("Iniciando ingestar imagen en bff")
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    context = BaseContext()
    context.request = request
    image_data = await image.read()
    imagen_base64 = base64.b64encode(image_data).decode('utf-8')
    id_correlacion=str(uuid.uuid4())
    query = """
    mutation ($imagenBase64: String!, $nombreImagen: String!, $proveedor: String!,$idCorrelacion:String!) {
        ingestarImagen(imagenBase64: $imagenBase64, nombreImagen: $nombreImagen, proveedor: $proveedor,idCorrelacion:$idCorrelacion) {
            mensaje
            codigo
            id
        }
    }
    """
    variables = {
        "imagenBase64": imagen_base64,
        "nombreImagen": image.filename,
        "proveedor": proveedor
        ,"idCorrelacion": id_correlacion
    }
    
    logger.info(f"antes de ejecutar la mutacion")
    result = await schema.execute(
        query,
        variable_values=variables,
        context_value=context,
    )

    despachador=Despachador()
    payload=InicioSagaPayload(mensaje="Inicio de la saga de ingesta de imagen")
    evento_inicio_saga=EventoIntegracionInicioSaga(data=payload,id_correlacion=id_correlacion)
    avro_schema=AvroSchema(EventoIntegracionInicioSaga)
    await despachador.publicar_mensaje_avro(mensaje=evento_inicio_saga,
                                      topico='eventos-bff',
                                      avro_schema=avro_schema)

    return Response(
        content=result.data["ingestarImagen"]["mensaje"],
        status_code=result.data["ingestarImagen"]["codigo"])
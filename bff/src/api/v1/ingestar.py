from fastapi import APIRouter, Request, UploadFile, Form, File, Response, Depends
from src.seedwork.aplicacion.autenticacion import token_required
from strawberry.fastapi.context import BaseContext
from .mutaciones import Mutation
import strawberry
from .consultas import Query
from io import BytesIO
import base64

router = APIRouter()

@router.post("/ingesta-imagen")
async def ingestar_imagen(
    request: Request,
    image: UploadFile = File(...),
    proveedor: str = Form(...),
    current_user: str = Depends(token_required)  # Use the token_required dependency
):
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    context = BaseContext()
    context.request = request
    image_data = await image.read()
    imagen_base64 = base64.b64encode(image_data).decode('utf-8')
    query = """
    mutation ($imagenBase64: String!, $nombreImagen: String!, $proveedor: String!) {
        ingestarImagen(imagenBase64: $imagenBase64, nombreImagen: $nombreImagen, proveedor: $proveedor) {
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
    }
    
    result = await schema.execute(
        query,
        variable_values=variables,
        context_value=context,
    )
    return Response(
        content=result.data["ingestarImagen"]["mensaje"],
        status_code=result.data["ingestarImagen"]["codigo"])
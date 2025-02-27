from src.seedwork.aplicacion.comandos import Comando
from src.aplicacion.dto import IngestaImagenDTO
from uuid import UUID
import pulsar
import json
from dataclasses import dataclass, field
from src.seedwork.aplicacion.comandos import ejecutar_commando as comando
from datetime import datetime

@dataclass
class IngestaImagen(Comando):
    fecha_creacion: str
    id: str
    filename: str
    size: str
    binario_url: str
    mimetype: str


class IngestaImagenHandler:
    def __init__(self):
        self.client = pulsar.Client('pulsar://localhost:6650')
        self.producer = self.client.create_producer('comando_ingesta_imagenes')

    def handle(self, comando: IngestaImagen):
        reserva_dto = IngestaImagenDTO(
                proveedor=comando.proveedor,
                fecha_creacion=comando.fecha_creacion,
                id=comando.id,
                filename=comando.filename,
                size=comando.size,
                binario_url=comando.binario_url,
                mimetype=comando.mimetype)
        self.process(reserva_dto)

    def process(self, dto: IngestaImagenDTO):
        # Convert DTO to JSON, ensuring datetime is serialized as a string
        dto_dict = dto.__dict__
        dto_dict['fecha_creacion'] = dto_dict['fecha_creacion'].isoformat() if isinstance(dto_dict['fecha_creacion'], datetime) else dto_dict['fecha_creacion']
        dto_dict['id'] = str(dto_dict['id']) if isinstance(dto_dict['id'], UUID) else dto_dict['id']
        dto_json = json.dumps(dto_dict)
        # Send the DTO to the Pulsar topic
        self.producer.send(dto_json.encode('utf-8'))
        print(f"Sent DTO to Pulsar: {dto_json}")

    def __del__(self):
        self.client.close()

@comando.register(IngestaImagen)
def ejecutar_comando_anonimizar_imagen(comando: IngestaImagen):
    handler = IngestaImagenHandler()
    handler.handle(comando)
    
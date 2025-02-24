from src.infraestructura.despachadores import Despachador
from src.seedwork.aplicacion.handlers import Handler

class HandlerAnonimizacionIntegracion(Handler):

    @staticmethod
    def handle_imagen_anonimizada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-anonimizador')
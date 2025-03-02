from src.infraestructura.despachadores import Despachador
from src.seedwork.aplicacion.handlers import Handler

#TODO revisar handler vs tutorial, handler admin evento escuchado no publica evento
class HandlerAnonimizacionIntegracion(Handler):
    @staticmethod
    def handle_imagen_anonimizada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-anonimizador')
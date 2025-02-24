from pydispatch import dispatcher

from .handlers import HandlerAnonimizacionIntegracion

from src.dominio.eventos import ImagenAnonimizada

dispatcher.connect(HandlerAnonimizacionIntegracion.handle_imagen_anonimizada, signal=f'{ImagenAnonimizada.__name__}Integracion')
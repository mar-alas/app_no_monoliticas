import os

def broker_host():
    """
    Obtiene el host del broker a partir de variables de entorno
    
    Returns:
        str: Host del broker (por defecto 'localhost')
    """
    return os.getenv('BROKER_HOST', 'localhost')
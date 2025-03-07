import os

def broker_host():
    return os.getenv('BROKER_HOST', 'localhost')
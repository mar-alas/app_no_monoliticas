from pulsar.schema import *
import uuid

class EventoIntegracion(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=0)
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
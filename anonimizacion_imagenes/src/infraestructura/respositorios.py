from src.infraestructura.dto import DTOImagenAnonimizada, DTOImagenAnonimizadaSchema
from src.config.db import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import os

DB_USERNAME = os.getenv('DB_USERNAME', default="user")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="password")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="9001")

engine = create_engine(
    f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/anonimizacion_db',
    pool_size=5,               # Reduce pool size to avoid too many connections
    max_overflow=2,
    pool_recycle=120,          # Recycle connections more frequently
    pool_timeout=30,           # Add a timeout for getting connections from pool
    pool_pre_ping=True,        # Keep pre_ping to detect stale connections
    connect_args={"connect_timeout": 10}  # Add connection timeout
)
class RepositorioImagenesAnonimizadasSQLAlchemy:
    def __init__(self):
            
        # Create a scoped session factory
        self.Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    
    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            # Remove session from registry to avoid leaks with scoped_session
            self.Session.remove()

    def almacenar_info_imagen_anonimizada(self, imagen: DTOImagenAnonimizada):
        with self.session_scope() as session:
            session.add(imagen)
            return imagen
    
    def obtener_inventario_imagenes_anonimizadas(self):
        with self.session_scope() as session:
            query_schema = DTOImagenAnonimizadaSchema()
            query = session.query(DTOImagenAnonimizada).all()
            results = query_schema.dump(query, many=True)
            return results
    
    def test_conexion(self):
        try:
            with self.engine.connect() as conn:
                return True
        except Exception:
            return False
            
    def almacenar_ejemplo(self):
        imagen = DTOImagenAnonimizada(
            fileName="imagen1.jpg",
        )
        self.almacenar_info_imagen_anonimizada(imagen)
        return True



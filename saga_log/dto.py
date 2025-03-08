from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class SagaLog(db.Model):
    __tablename__ = 'saga_logs'
    id = db.Column(db.Integer, primary_key=True)
    id_correlacion = db.Column(db.String(50))
    evento = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'evento': self.evento,
            'timestamp': self.timestamp.isoformat(),
        }

class SagaLogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SagaLog
        include_fk = True
        load_instance = True
        sqla_session = db.session

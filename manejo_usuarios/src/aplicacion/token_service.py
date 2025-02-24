import jwt
from datetime import datetime, timedelta

SECRET_KEY = "secreto_super_seguro"

class TokenService:
    @staticmethod
    def generate_token(user_id: str):
        payload = {
            "sub": str(user_id),
            "exp": datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

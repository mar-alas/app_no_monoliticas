import jwt
from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# TODO: poner secret key en variable de entorno
SECRET_KEY = "secreto_super_seguro"  # misma clave que en manejo_usuarios

security = HTTPBearer()

async def token_required(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        current_user = payload["sub"]
        return current_user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token is expired!")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token!")
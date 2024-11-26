from fastapi import HTTPException
import jwt

secret = "iluvanushka"
ALGORITHM = "HS256"

def decode_token(token):
    try:
        payload = jwt.decode(token, secret, algorithms=ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
        


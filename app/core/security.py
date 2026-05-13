import jwt
from jwt import PyJWTError, ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRES_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES')


pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def create_access_token(data:dict):
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    data.update({"exp":expire})
    return jwt.encode(data, SECRET_KEY, ALGORITHM)



def verify_access_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
        return {"valid": True, "payload": payload}
    except ExpiredSignatureError:
        return {"valid": False, "error": "token_expired"}
    except InvalidTokenError:
        return {"valid": False, "error": "invalid_token"}
    except Exception as e:
        return {"valid": False, "error": str(e)}
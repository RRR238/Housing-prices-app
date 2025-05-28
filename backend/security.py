import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
import bcrypt


class SecurityConfig:
    SECRET_KEY = "SuperSecretKey"
    ALGORITHM = "HS256"
    ISSUER = "http://127.0.0.1:5000"
    AUDIENCE = "FastAPI"
    oauth2Scheme = OAuth2PasswordBearer(tokenUrl="login")

class SecurityManager:

    def __init__(self):
        self.SECRET_KEY = SecurityConfig.SECRET_KEY
        self.ALGORITHM = SecurityConfig.ALGORITHM
        self.ISSUER = SecurityConfig.ISSUER
        self.AUDIENCE = SecurityConfig.AUDIENCE

    def HashPassword(self,
                     plain_password: str) -> str:

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def VerifyPassword(self,
                       plain_password: str,
                       hashed_password: str) -> bool:

        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


    def CreateJWTToken(self,
                       data: dict,
                       expires_delta: timedelta = timedelta(hours=1)) -> str:

        to_encode = data.copy()

        # Add expiration time if specified
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)  # Default to 15 minutes
        to_encode.update({"exp": expire, "iss":self.ISSUER, "aud":self.AUDIENCE})

        # Create and sign the JWT token
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm = self.ALGORITHM)
        return token


def EndpointVerification(token: str = Depends(SecurityConfig.oauth2Scheme)):

    try:
        # Decode the JWT token
        payload = jwt.decode(token, SecurityConfig.SECRET_KEY, algorithms=[SecurityConfig.ALGORITHM],
                             audience=SecurityConfig.AUDIENCE, issuer = SecurityConfig.ISSUER)
        return payload  # Return the decoded token (you can access user info like "sub", "role", etc.)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except (jwt.InvalidTokenError, jwt.DecodeError, jwt.PyJWTError):
        raise HTTPException(status_code=401, detail="Invalid or malformed token")
from passlib.context import CryptContext
from jose import jwt, JWTError

from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import OAuth2PasswordBearer

from datetime import (
    datetime,
    timedelta,
    timezone
)

from app.config import settings

#JWT settings
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = (
    settings.ACCESS_TOKEN_EXPIRE_MINUTES
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

#password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

#JWT token creation

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

#JWT token verification
def verify_access_token(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")
        email = payload.get("email")
        role = payload.get("role")

        if not user_id or not email or not role:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        return payload

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


#Role based access
def require_role(required_role: str):

    def role_checker(
        user_data: dict = Depends(
            verify_access_token
        )
    ):

        user_role = user_data.get("role")

        if user_role != required_role:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

        return user_data

    return role_checker


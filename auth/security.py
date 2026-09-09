from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from jose import JWTError, jwt


# =========================================================
# PASSWORD HASHING
# =========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


# =========================================================
# JWT CONFIGURATION
# =========================================================

SECRET_KEY = "TRAVELX_SECRET_KEY_2026_CHANGE_ME"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


# =========================================================
# HTTP BEARER
# =========================================================

security = HTTPBearer()


# =========================================================
# CREATE ACCESS TOKEN
# =========================================================

def create_access_token(user_id: int, email: str) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# =========================================================
# GET CURRENT USER
# =========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")
        email = payload.get("email")

        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        return {
            "id": int(user_id),
            "email": email
        }

    except (JWTError, ValueError, TypeError):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
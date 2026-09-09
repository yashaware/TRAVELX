from pydantic import BaseModel
from typing import Optional


# =========================================================
# REGISTER
# =========================================================

class UserRegister(BaseModel):

    name: str
    email: str
    phone: str
    password: str


# =========================================================
# LOGIN
# =========================================================

class UserLogin(BaseModel):

    email: str
    password: str


# =========================================================
# TOKEN RESPONSE
# =========================================================

class TokenResponse(BaseModel):

    access_token: str
    token_type: str


# =========================================================
# PROFILE UPDATE
# =========================================================

class ProfileUpdate(BaseModel):

    name: Optional[str] = None
    phone: Optional[str] = None
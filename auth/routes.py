from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import User

from auth.schemas import (
    UserRegister,
    UserLogin,
    TokenResponse,
    ProfileUpdate
)

from auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)


# =========================================================
# AUTHENTICATION ROUTER
# =========================================================

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================================================
# REGISTER
# =========================================================

@auth_router.post("/register")
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):

    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(
        user_data.password
    )

    # Create new user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        password=hashed_password,
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully 🎉",
        "user_id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }


# =========================================================
# LOGIN
# =========================================================

@auth_router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):

    # Find user by email
    user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    # Check user
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(
        user_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
        role=user.role or "user"
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================================================
# GET PROFILE
# =========================================================

@auth_router.get("/profile")
def profile(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Find current user in database
    user = db.query(User).filter(
        User.id == current_user["id"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "Welcome to your TRAVELX profile 🎉",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone
        }
    }


# =========================================================
# UPDATE PROFILE
# =========================================================

@auth_router.put("/profile")
def update_profile(
    profile_data: ProfileUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # Find current user
    user = db.query(User).filter(
        User.id == current_user["id"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Update name
    if profile_data.name is not None:
        user.name = profile_data.name

    # Update phone
    if profile_data.phone is not None:
        user.phone = profile_data.phone

    # Save changes
    db.commit()
    db.refresh(user)

    return {
        "message": "Profile updated successfully 🎉",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone
        }
    }
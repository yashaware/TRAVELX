from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.database import engine, Base
from db import models

from auth.routes import auth_router
from buses.routes import bus_router
from wallet.routes import wallet_router
from bookings.routes import booking_router


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

Base.metadata.create_all(
    bind=engine
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="TRAVELX API",
    description=(
        "TRAVELX - All-in-One Travel & Lifestyle "
        "Super App"
    ),
    version="2.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =========================================================
# ROUTERS
# =========================================================

app.include_router(
    auth_router
)

app.include_router(
    bus_router
)

app.include_router(
    wallet_router
)

app.include_router(
    booking_router
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to TRAVELX 🚀",
        "status": "API is running successfully",
        "version": "2.0.0"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "TRAVELX API"
    }
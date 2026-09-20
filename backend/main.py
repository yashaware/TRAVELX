import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine, Base
from db import models
from auth.routes import auth_router
from buses.routes import bus_router
from wallet.routes import wallet_router
from bookings.routes import booking_router
from trains.routes import train_router
from hotels.routes import hotel_router
from flights.routes import flight_router
from cabs.routes import cab_router
from food.routes import food_router
from movies.routes import movie_router
from events.routes import event_router
from notifications.routes import notification_router
from admin.routes import admin_router
# ============================================================
# LOAD ENVIRONMENT
# ============================================================
load_dotenv()
# ============================================================
# CREATE DATABASE TABLES
# ============================================================
Base.metadata.create_all(
    bind=engine
)
# ============================================================
# FASTAPI APPLICATION
# ============================================================
app = FastAPI(
    title="TRAVELX API",
    description=(
        "TRAVELX - All-in-One "
        "Travel & Lifestyle Super App"
    ),
    version="2.0.0"
)
# ============================================================
# CORS
# ============================================================
cors_origins_raw = os.getenv(
    "TRAVELX_CORS_ORIGINS",
    "http://localhost:8501,http://127.0.0.1:8501"
)
cors_origins = [
    origin.strip()
    for origin in cors_origins_raw.split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# ============================================================
# ROUTERS
# ============================================================
app.include_router(auth_router)
app.include_router(bus_router)
app.include_router(wallet_router)
app.include_router(booking_router)
app.include_router(train_router)
app.include_router(hotel_router)
app.include_router(flight_router)
app.include_router(cab_router)
app.include_router(food_router)
app.include_router(movie_router)
app.include_router(event_router)
app.include_router(notification_router)
app.include_router(admin_router)
# ============================================================
# HOME
# ============================================================
@app.get("/")
def home():
    return {
        "message": "Welcome to TRAVELX ??",
        "status": "API is running successfully",
        "version": "2.0.0"
    }
# ============================================================
# HEALTH CHECK
# ============================================================
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "TRAVELX API"
    }
@app.get("/debug/db")
def debug_db():
    return {
        "database": engine.url.database,
        "host": engine.url.host,
        "username": engine.url.username,
        "driver": engine.url.drivername
    }
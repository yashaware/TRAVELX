from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)

    phone = Column(String, nullable=True)

    password = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
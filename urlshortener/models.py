from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from .database import Base


class URL(Base):
    __tablename__ = 'urls'

    id = Column(String, primary_key=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now())

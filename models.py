from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base
from sqlalchemy.sql import func

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(Text)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
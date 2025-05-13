from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime

Base = declarative_base()

class PersonDB(Base):
    __tablename__ = "persons"
    id = Column(String, primary_key=True)
    name = Column(String)
    photo_url = Column(String)
    cause_of_death = Column(String, default="Ataque al corazón")
    death_details = Column(String, nullable=True)
    is_dead = Column(Boolean, default=False)
    time_of_death = Column(DateTime, nullable=True)

class PersonCreate(BaseModel):
    name: str
    photo_url: str
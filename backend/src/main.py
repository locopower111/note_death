from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from src.models import Base, PersonCreate, PersonDB # Importamos ambos modelos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import shutil
import os
import uuid

app = FastAPI()
DATABASE_URL = "postgresql://postgres:postgres@db/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, bind=engine)
Base.metadata.create_all(bind=engine)

def create_person(db, person_data: PersonCreate):
    db_person = PersonDB(
        id=str(uuid.uuid4()),
        name=person_data.name,
        photo_url=person_data.photo_url
    )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@app.post("/persons")
async def register_person(name: str, photo: UploadFile = File(...)):
    # Guardar foto
    os.makedirs("uploads", exist_ok=True)
    photo_path = f"uploads/{photo.filename}"
    with open(photo_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
    
    db = SessionLocal()
    person_data = PersonCreate(name=name, photo_url=photo_path)
    person = create_person(db, person_data)
    db.close()
    return person
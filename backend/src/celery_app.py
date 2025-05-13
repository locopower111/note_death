from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Configuración robusta de Celery
app = Celery(
    'tasks',
    broker='amqp://guest:guest@rabbitmq',
    backend='rpc://',
    broker_connection_retry_on_startup=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True
)

# Conexión a DB (ajusta según tu configuración)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db/postgres")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, bind=engine)

@app.task(name="schedule_death")
def schedule_death(person_id: str):
    db = SessionLocal()
    try:
        person = db.query(PersonDB).filter(PersonDB.id == person_id).first()
        if person and not person.is_dead:
            person.is_dead = True
            person.time_of_death = datetime.now()
            db.commit()
    finally:
        db.close()
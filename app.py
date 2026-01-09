from fastapi import FastAPI

from database import engine
from models.base import Base

import models.user
import models.trainer
import models.gym_class
import models.user_class

app = FastAPI(
    title="Gym Management API"
)

# OJO Esto crea las tablas la primera vez que se ejecuta la aplicación
# @app.on_event("startup")
# def startup():
#     Base.metadata.create_all(bind=engine)
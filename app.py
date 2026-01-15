from fastapi import FastAPI, Request 
from fastapi.responses import JSONResponse

from config.exceptions import AppException, NotFoundException,InvalidDataException


from database import engine
from models.base import Base
from routes.users_routes import router as users_router
from routes.trainers_routes import router as trainers_router
from routes.classes_routes import router as classes_router

import models.user
import models.trainer
import models.gym_class
import models.user_class

app = FastAPI(
    title="Gym Management API"
)

app.include_router(users_router)
app.include_router(trainers_router)
app.include_router(classes_router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.exception_handler(NotFoundException) # recurso no encontrado 404
async def not_found_exception_handler(
    request: Request,
    exc: NotFoundException
):
    return JSONResponse(
        status_code=404,
        content={
            "error": "NotFound",
            "message": exc.message
        }
    )

@app.exception_handler(InvalidDataException) #Datos invalidos 400 
async def invalid_data_exception_handler(
    request: Request,
    exc: InvalidDataException
):
    return JSONResponse(
        status_code=400,
        content={
            "error": "InvalidData",
            "message": exc.message
        }
    )
# Handler base para cualquier otra AppException → 400
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=400,
        content={
            "error": "ApplicationError",
            "message": exc.message
        }
    )
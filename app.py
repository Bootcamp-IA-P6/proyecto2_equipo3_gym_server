from fastapi import FastAPI, Request 
from fastapi.responses import JSONResponse

from config.exceptions import AppException, NotFoundException,InvalidDataException


from database import engine
from models.base import Base
from routes.users_routes import router as users_router
from routes.user_class_routes import router as user_class_router
from routes.trainers_routes import router as trainers_router
from routes.classes_routes import router as classes_router
from config.logger import setup_logger, get_logger

import models.user
import models.trainer
import models.gym_class
import models.user_class


setup_logger()
logger = get_logger("app")

app = FastAPI(
    title="Gym Management API"
)

app.include_router(users_router)
app.include_router(user_class_router)
app.include_router(trainers_router)
app.include_router(classes_router)

@app.on_event("startup")
def startup():
    logger.info("Application started")
    Base.metadata.create_all(bind=engine)

#Handler global único
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    # Definir status code y tipo de error según el tipo de excepción
    if isinstance(exc, NotFoundException):
        status_code = 404
        error_type = "NotFound"
    elif isinstance(exc, InvalidDataException):
        status_code = 400
        error_type = "InvalidData"
    else:
        status_code = 400
        error_type = "ApplicationError"

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": error_type,
            "message": exc.message  # tu exceptions.py usa self.message
        }
    )
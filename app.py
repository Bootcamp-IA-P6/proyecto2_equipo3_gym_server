from fastapi import FastAPI, Request 
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from config.logger import setup_logger, get_logger
from config.exceptions import AppException, NotFoundException,InvalidDataException

from database import engine
from models.base import Base
from routes.users_routes import router as users_router
from routes.user_class_routes import router as user_class_router
from routes.trainers_routes import router as trainers_router
from routes.classes_routes import router as classes_router
from routes.auth_routes import router as auth_router
from config.settings import settings


import models.user
import models.trainer
import models.gym_class
import models.user_class


setup_logger()
logger = get_logger("app")

app = FastAPI(
    title="Gym Management API 🏋️‍♂️",
    description= """API para la gestión integral de un gimnasio.
    Permite administrar **Usuarios**, **Entrenadores** e **Clases**.

    Producido por el Equipo 3: Gema, Iris, Juan, Naizabeth.
    """,
    version="1.0.0",
    contact={
        "name": "Nexafit Labs - Consultoría tecnológica para el sector fitness",
        "url": "http://nexafit-labs.tech/support",
    }
)

# CONFIGURAR CORS CON ENV ---
# Convertimos el string "url1,url2" en una lista ["url1", "url2"]
origins = settings.ALLOWED_ORIGINS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Qué dominios pueden hablar con tu API
    allow_credentials=True,     # Permitir cookies/tokens de autenticación
    allow_methods=["*"],        # Permitir todos los métodos (GET, POST, PUT, DELETE...)
    allow_headers=["*"],        # Permitir todos los headers
)

app.include_router(users_router)
app.include_router(user_class_router)
app.include_router(trainers_router)
app.include_router(classes_router)
app.include_router(auth_router)

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
        # Logueamos como warning porque es un error del usuario (pidió algo que no existe)
        logger.warning(f"Recurso no encontrado: {exc.message}")
    elif isinstance(exc, InvalidDataException):
        status_code = 400
        error_type = "InvalidData"
        logger.warning(f"Datos inválidos recibidos: {exc.message}")
    else:
        status_code = 400
        error_type = "ApplicationError"
        # Logueamos como error porque es algo inesperado de la app
        logger.error(f"Error de aplicación: {exc.message}")

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": error_type,
            "message": exc.message  # tu exceptions.py usa self.message
        }
    )
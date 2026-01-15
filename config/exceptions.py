#En este archivo vamos a observar que tipo de error ocurrio 
# config/exceptions.py

class AppException(Exception):
    """Excepción base de la aplicación"""
    def __init__(self, message: str):
        self.message = message


class NotFoundException(AppException):
    """Cuando un recurso no existe"""
    pass


class InvalidDataException(AppException):
    """Cuando los datos enviados no son válidos"""
    pass
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user_class import UserClass
from schemas.user_class_schema import UserClassCreate

from models.user import User
from models.trainer import Trainer
from models.gym_class import GymClass

import pandas as pd
import datetime
from fastapi.responses import FileResponse
import os

def list_objects_to_csv(db: Session, list_user_class: list[UserClass], user_id_file: str):
    # Lista de user_class vacia
    users_class = []

    for user in list_user_class:
        # Usuario vacio
        user_aux = {
            "id": 0,
            "user_id": 0,
            "user_name": "",
            "class_id": 0,
            "class_name": "",
            "trainer_id": 0,
            "trainer_name": ""
        }

        user_aux['id'] = user.id

        user_aux['user_id'] = user.user_id
        # Busca el nombre de usuario
        user_find = db.query(User).filter(User.id == user.user_id).first()
        user_aux['user_name'] = user_find.name

        user_aux['class_id'] = user.class_id
        # Busca el nombre de la clase
        class_find = db.query(GymClass).filter(GymClass.id == user.class_id).first()
        user_aux['class_name'] = class_find.name

        user_aux['trainer_id'] = user.trainer_id
        # Busca el nombre del entrenador
        trainer_find = db.query(User).filter(User.id == user.trainer_id).first()
        user_aux['trainer_name'] = trainer_find.name

        users_class.append(user_aux)

    # Crea el DataFrame 
    df_users = pd.DataFrame(users_class)
    # Crea el nombre del fichero
    file_csv = file_name_csv(user_id_file)
    # Guarda el fichero csv en la carpeta docs/csv del Backend
    df_users.to_csv('docs/csv/' + file_csv, index=False, encoding='utf-8')

    return file_name_download_csv(file_csv)

def file_name_csv(user_id_file: str):
    file_name = "datcsv_"

    # Obtener la fecha actual
    today = datetime.datetime.now()

    # Formatear la fecha como una cadena (AAAA-MM-DD)
    formatted_date = today.strftime("%Y-%m-%d-%H-%M")

    if user_id_file == "all":
        file_name += formatted_date + "_user_all.csv"
    else:
        file_name += formatted_date + "_user_" + user_id_file + ".csv"

    return file_name

def file_name_download_csv(file_name_download: str):
    file_path = os.path.join("docs\csv", file_name_download) # Ruta al archivo

    return FileResponse(path=file_path, filename=file_name_download)
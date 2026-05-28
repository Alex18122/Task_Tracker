import argparse
from datetime import date
import json
from typing import Optional
from pydantic import BaseModel


class Data(BaseModel):
    id: Optional[str] = None
    description: Optional[str] = None
    status: str
    createdAt: date
    udatedAt: date

false_db = []

def comandos_entrada_parser(data: Data):

    parser = argparse.ArgumentParser(prog= "task-cli")
    subparser = parser.add_subparsers(dest= "comando")

    #task-cli add  "tarea a realizar"
    add_parser = subparser.add_parser("add", help= "agrega una tarea a la lista")
    add_parser.add_argument("descripcion",help= "escibir lo que es la tarea a realizar")

    #task-cli list 
    list_parser = subparser.add_parser("list", help = "muestra todas las tareas de la lista")
    list_parser.add_argument("--status", help = "filtra las tareas por estado (pendiente, en progreso, hecha)")

    #task-li update 1 "tarea actualizada"
    update_parser = subparser.add_parser("update", help = "actualiza una tarea de la lista")
    update_parser.add_argument("id", help = "escribir el id de la tarea a actualizar")
    update_parser.add_argument("descripcion", help = "escribir la nueva descripcion de la tarea")

    #task-cli delete 1
    delete_parser = subparser.add_parser("delete", help = "elimina una tarea de la lista")
    delete_parser.add_argument("id", help = "escribir el id de la tarea a eliminar")

    #task-cli mark-in-progress 1
    mark_in_progress_parser = subparser.add_parser("mark-in-progress", help = "marca una tarea como en progreso")
    mark_in_progress_parser.add_argument("id", help = "escribir el id de la tarea a marcar como en progreso")

    #task-cli mark-done 1
    mark_done_parser = subparser.add_parser("mark-done", help = "marca una tarea como hecha")
    mark_done_parser.add_argument("id", help = "escribir el id de la tarea a marcar como hecha")


parser = comandos_entrada_parser(Data)
   

def taskcli():

    print("Administrador De Tareas")
    print("----------------------------------------------------------------------------------------------")
    
    

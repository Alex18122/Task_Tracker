import argparse
from datetime import datetime
import shlex
from typing import Optional
from pydantic import BaseModel , Field

contador_id = 1

class Data(BaseModel):
    id: int
    description: str
    status: str
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: Optional[datetime] = None

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
    update_parser.add_argument("id",type=int ,help = "escribir el id de la tarea a actualizar")
    update_parser.add_argument("descripcion", help = "escribir la nueva descripcion de la tarea")

    #task-cli delete 1
    delete_parser = subparser.add_parser("delete", help = "elimina una tarea de la lista")
    delete_parser.add_argument("id",type=int , help = "escribir el id de la tarea a eliminar")

    #task-cli mark-in-progress 1
    mark_in_progress_parser = subparser.add_parser("mark-in-progress", help = "marca una tarea como en progreso")
    mark_in_progress_parser.add_argument("id",type=int , help = "escribir el id de la tarea a marcar como en progreso")

    #task-cli mark-done 1
    mark_done_parser = subparser.add_parser("mark-done", help = "marca una tarea como hecha")
    mark_done_parser.add_argument("id",type=int , help = "escribir el id de la tarea a marcar como hecha")

    return parser


parser = comandos_entrada_parser(Data)
   
def agregar_tarea(descripcion: str):
    
    global contador_id 
    tarea = Data(id=contador_id, description= descripcion,status="ToDo")
    
    false_db.append(tarea)

    return tarea

def modificar_tarea(id: int, descripcion: str):

    for tarea in false_db:
        if tarea.id == id:
            tarea.description = descripcion
            tarea.updatedAt = datetime.now()
            false_db[id-1] = tarea
            print(false_db[id-1])
            return tarea
    print(false_db[id-1])

def taskcli():

    print("Administrador De Tareas")
    print("---------------------------------------------------------------")
    
    while True:
        entrada = input(">> ")
        partes = shlex.split(entrada) # divide la entrada en partes, respetando las comillas
        args = parser.parse_args(partes[1:] ) #parsea las partes de la entrada, omitiendo el primer elemento que es "task-cli"

        if args.comando == "add":

            tar= agregar_tarea(args.descripcion)
            print(f"tarea {tar.id}:'{args.descripcion}' agregada a la lista")
            print(f"estado de la tarea {tar.id} : {tar.status}")
        elif args.comando == "update":

            tar = modificar_tarea(args.id, args.descripcion)
            #print(false_db)

taskcli()
    
    

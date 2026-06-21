import argparse
from datetime import datetime
import json
from pathlib import Path
import shlex
from typing import Optional
from pydantic import BaseModel, Field

contador_id: int

class Data(BaseModel):

    id: int
    description: str
    status: str
    createdAt: datetime = Field(default_factory=datetime.now)
    updatedAt: Optional[datetime] = None

ARCHIVO = "tareas.json"

def guardar_tareas():

    datos = [tarea.model_dump() for tarea in false_db ]
    with open(ARCHIVO, "w") as f:
        json.dump(datos, f , indent = 2, default=str)

def cargar_tareas():

    if not Path(ARCHIVO).exists():
        
        return []
    
    with open(ARCHIVO, "r") as f:

        datos = json.load(f)

    return [Data(**d) for d in datos]

def comandos_entrada_parser():

    parser = argparse.ArgumentParser(prog="task-cli")
    subparser = parser.add_subparsers(dest="comando")

    # task-cli add  "tarea a realizar"
    add_parser = subparser.add_parser("add", help="agrega una tarea a la lista")
    add_parser.add_argument("descripcion", help="escibir lo que es la tarea a realizar")

    # task-cli list
    list_parser = subparser.add_parser("list", help="muestra todas las tareas de la lista")
    list_parser.add_argument("--status", help="filtra las tareas por estado (pendiente, en progreso, hecha)")

    # task-li update 1 "tarea actualizada"
    update_parser = subparser.add_parser("update", help="actualiza una tarea de la lista")
    update_parser.add_argument("id", type=int, help="escribir el id de la tarea a actualizar")
    update_parser.add_argument(   "descripcion", help="escribir la nueva descripcion de la tarea")

    # task-cli delete 1
    delete_parser = subparser.add_parser("delete", help="elimina una tarea de la lista")
    delete_parser.add_argument("id", type=int, help="escribir el id de la tarea a eliminar")

    # task-cli mark-in-progress 1
    mark_in_progress_parser = subparser.add_parser("mark-in-progress", help="marca una tarea como 'en progreso'")
    mark_in_progress_parser.add_argument("id", type=int, help="escribir el id de la tarea a marcar como 'en progreso'")

    # task-cli mark-done 1
    mark_done_parser = subparser.add_parser("mark-done", help="marca una tarea como hecha")
    mark_done_parser.add_argument("id", type=int, help="escribir el id de la tarea a marcar como hecha")

    return parser

parser = comandos_entrada_parser()
false_db = cargar_tareas()

def generar_id():

    if not false_db:

        return 1

    return max(tar.id for tar in false_db) + 1

def agregar_tarea(descripcion: str):

    tarea = Data(id=generar_id(), description=descripcion, status="ToDo")

    false_db.append(tarea)

    return tarea

def modificar_tarea(id: int, descripcion: str):

    for tarea in false_db:

        if tarea.id == id:

            tarea.description = descripcion
            tarea.updatedAt = datetime.now()
            false_db[id - 1] = tarea
            
            return True
    return False

def eliminar_tarea(id:int):

    for tarea in false_db:

        if tarea.id == id:

            false_db.remove(tarea)
            print(f"tarea {tarea.id} eliminada exitosaente")
            return True
        
    return False

def listar_tareas():

    print("\n Lista de tareas")
    print("------------------------------")

    for tarea in false_db:

        print(f"id : {tarea.id}\n")
        print(f"Tarea : {tarea.description}")
        print(f"Estado : {tarea.status}")
        print(f"fecha de creacion : {tarea.createdAt}")
        
        if tarea.updatedAt is not None:

            print(f"Fecha de modificacion : {tarea.updatedAt}")

        print("---------------------------------------------------------------") 

def listar_tareas_hechas():

    print("\n lista de tareas hechas")
    print("------------------------------")

    for tarea in false_db:

        if tarea.status == "Done":

            print(f"id : {tarea.id}\n")
            print(f"Tarea : {tarea.description}")
            print(f"Estado : {tarea.status}")
            print(f"fecha de creacion : {tarea.createdAt}")

            if tarea.updatedAt is not None:

                print(f"fecha de modificacion : {tarea.updatedAt}")

        print("---------------------------------------------------------------") 

def listar_tareas_por_hacer():

    print("\n lista de tareas por hacer")
    print("------------------------------")

    for tarea in false_db:

        
        if tarea.status == "ToDo":

            print(f"id : {tarea.id}\n")
            print(f"Tarea : {tarea.description}")
            print(f"Estado : {tarea.status}")
            print(f"fecha de creacion : {tarea.createdAt}")

            if tarea.updatedAt is not None:

                print(f"fecha de modificacion : {tarea.updatedAt}")
        
        print("---------------------------------------------------------------") 

def listar_tareas_en_prog():

    print("\n lista de tareas en progreso")
    print("------------------------------")

    for tarea in false_db:

        if tarea.status == "In Progress":

            print(f"id : {tarea.id}\n")
            print(f"Tarea : {tarea.description}")
            print(f"Estado : {tarea.status}")
            print(f"fecha de creacion : {tarea.createdAt}")

            if tarea.updatedAt is not None:

                print(f"fecha de modificacion : {tarea.updatedAt}")  

        print("---------------------------------------------------------------")  

def marcar_tarea_hecha(id: int):

    for tarea in false_db:

        conta = 0

        if tarea.id == id:

            tarea.status = "Done"
            false_db[id - 1] = tarea
            print(f"Tarea {tarea.id} marcada como hecha ")

        else:

            conta += 1

            if conta == len(false_db):

                print("Tarea no encontrada.")

def marcar_tarea_en_progreso(id: int):

    for tarea in false_db:

        conta = 0

        if tarea.id == id:

            tarea.status = "In Progress"
            false_db[id - 1] = tarea
            print(f"Tarea {tarea.id} marcada como 'en progreso' ")

        else:

            conta += 1

            if conta == len(false_db):

                print("Tarea no encontrada.")

def taskcli():

    print("Administrador De Tareas")
    print("---------------------------------------------------------------")

    while True:
        
        entrada = input(">> ")

        partes = shlex.split(entrada)  # divide la entrada en partes, respetando las comillas
        args = parser.parse_args(partes[1:])  # parsea las partes de la entrada, omitiendo el primer elemento que es "task-cli"

        if args.comando == "add":

            tar = agregar_tarea(args.descripcion)
            guardar_tareas()
            print(f"tarea {tar.id}:'{args.descripcion}' agregada a la lista")
            print(f"estado de la tarea {tar.id} : {tar.status}")

        elif args.comando == "update":

            tar = modificar_tarea(args.id, args.descripcion)

            if tar:

                guardar_tareas()
                print(f"tarea {args.id}:'{args.descripcion}' modificada exitosamente")

            else:

                print("id no encontrada")

        elif args.comando == "list":

            listar_tareas()

        elif args.comando == "mark-done":

            marcar_tarea_hecha(args.id)
            guardar_tareas()

        elif args.comando == "mark-in-progress":

            marcar_tarea_en_progreso(args.id)
            guardar_tareas()

        elif args.comando == "delete":

            eliminar_tarea(args.id)
            guardar_tareas()

        elif args.comando == "list done":

            listar_tareas_hechas()
        
        elif args.comando == "list todo":

            listar_tareas_por_hacer()
        
        elif args.comando == "list in progress":

            listar_tareas_en_prog()

        else:

            print("comando desconocido, intenta de nuevo.")

taskcli()
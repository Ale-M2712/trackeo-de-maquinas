import os
import sys
import sqlalchemy

def crear_db():#(anda) crea la base de datos y las tablas ,si ya existen no hace nada
    engine = sqlalchemy.create_engine("sqlite:///maquinas.db")#crea la base de datos ,si no existe ,si existe no hace nada
    with engine.connect() as connection:#conecta a la base de datos
        connection.execute(sqlalchemy.text('''
            CREATE TABLE IF NOT EXISTS maquinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                estado TEXT NOT NULL,
                modelo TEXT NOT NULL,
                marca TEXT NOT NULL,
                costo REAL NOT NULL

            )
        ''')
        )
        connection.commit()#guarda los cambios en la base de datos
        connection.execute(sqlalchemy.text('''
            CREATE TABLE IF NOT EXISTS incidentes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                maquina_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                estado TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                costos REAL NOT NULL,
                tiempo_de_parada INTEGER NOT NULL,
                FOREIGN KEY (maquina_id) REFERENCES maquinas (id)
            )
        ''')
        )
        connection.commit()#guarda los cambios en la base de datos
        print("Base de datos creada correctamente")

def agregar_maquina(nombre, estado, modelo, marca, costo):#(anda) agrega una maquina a la base de datos
    engine = sqlalchemy.create_engine("sqlite:///maquinas.db")
    with engine.connect() as connection:
        connection.execute(sqlalchemy.text('''
            INSERT INTO maquinas (nombre, estado, modelo, marca, costo) 
            VALUES (:nombre, :estado, :modelo, :marca, :costo)
        '''), {"nombre": nombre, "estado": estado, "modelo": modelo, "marca": marca, "costo": costo})
        connection.commit()

#en el programa vamos a usar una funcion antes para saber si es ahora o la hora es otra con datetime
def agregar_incidente(maquina_id, fecha, estado, descripcion, costos, tiempo_de_parada): #(anda) agrega un incidente 
    engine = sqlalchemy.create_engine("sqlite:///maquinas.db")
    with engine.connect() as connection:
        connection.execute(sqlalchemy.text('''
            INSERT INTO incidentes (maquina_id, fecha, estado, descripcion, costos, tiempo_de_parada) 
            VALUES (:maquina_id, :fecha, :estado, :descripcion, :costos, :tiempo_de_parada)
        '''), {"maquina_id": maquina_id, "fecha": fecha, "estado": estado, "descripcion": descripcion, "costos": costos, "tiempo_de_parada": tiempo_de_parada})
        connection.commit()

def eliminar_maquina(maquina_id):#(anda) elimina la maquina con el id dado
    engine = sqlalchemy.create_engine("sqlite:///maquinas.db")
    with engine.connect() as connection:
        connection.execute(sqlalchemy.text('''
            DELETE FROM maquinas WHERE id = :maquina_id
        '''), {"maquina_id": maquina_id})
        connection.commit()
    print(f"Máquina con ID {maquina_id} eliminada correctamente")

def obtener_maquinas():#(anda) obtiene todas las maquinas de la base de datos
    engine = sqlalchemy.create_engine("sqlite:///maquinas.db")
    with engine.connect() as connection:
        result = connection.execute(sqlalchemy.text('''
            SELECT id FROM maquinas
        '''))
        return [row[0] for row in result.fetchall()] #devuelve una lista con los nombres de las maquinas
def extraer_segun_id(maquina_id ,dato):
    engine = sqlalchemy.create_engine("sqlite:///maquinas.db")
    with engine.connect() as connection:
        result = connection.execute(sqlalchemy.text(f'''
            SELECT {dato} FROM maquinas WHERE id = :maquina_id
        '''), {"maquina_id": maquina_id})
        return result.fetchone()[0] #devuelve el dato solicitado de la maquina con el id dado
    
def acceder_a_img (maquina_id):
    nombre_carpeta = f"maquina_{maquina_id}"
    ruta_img = os.path.join(nombre_carpeta, "foto.jpg")
    if os.path.exists(ruta_img):
        print(f"Imagen encontrada para la máquina con ID {maquina_id}: {ruta_img}")
        return ruta_img
    else:
        print(f"No se encontró la imagen para la máquina con ID {maquina_id}.")
        return None
def obtener_incidentes(maquina_id): #id maquina fecha(dd-mm-aaaa hh-mm-ss) estado descripcion costos tiempo_de_parada
    engine = sqlalchemy.create_engine("sqlite:///maquinas.db")
    with engine.connect() as connection:
        result = connection.execute(sqlalchemy.text('''
            SELECT * FROM incidentes WHERE maquina_id = :maquina_id
        '''), {"maquina_id": maquina_id})
        return result.fetchall() #devuelve una lista con los incidentes de la maquina con el id dado
    
def mostrar_tabla():
    engine = sqlalchemy.create_engine("sqlite:///maquinas.db")
    with engine.connect() as connection:
        result = connection.execute(sqlalchemy.text('''
            SELECT * FROM maquinas
        '''))
        for row in result.fetchall():
            print(row)
def tabla_maquinas():
    engine = sqlalchemy.create_engine("sqlite:///maquinas.db")
    with engine.connect() as connection:
        result = connection.execute(sqlalchemy.text('''
            SELECT * FROM maquinas
        '''))
        return result.fetchall() #devuelve una lista con todas las maquinas de la base de datos
#test
# if __name__ == "__main__":
#     crear_db() #ok
#     #agregar_maquina("freza", "Operativo", "T-1000", "MarcaX", 5000.00) #ok ,agrega otra maquina igual si corre varias veces
#     #agregar_incidente(2, "2024-06-01", "Resuelto", "Falla en el motor", 200.00, 4) #ok
#     #eliminar_maquina(1) #ok ,elimina la maquina con id 1
#     print(obtener_maquinas()) #ok ,muestra todas las maquinas en la base de datos
#     for id in obtener_maquinas():
#         print(extraer_segun_id(id, "nombre")) #ok ,muestra el nombre de cada maquina en la base de datos
#     print("listo") 
#     # for id_maquina in obtener_maquinas():
#     #     nombre_carpeta = f"maquina_{id_maquina}"
#     #     os.makedirs(nombre_carpeta, exist_ok=True)
#     #     print(f"Carpeta creada: {nombre_carpeta}")


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

def obtener_maquinas():#(anda) obtiene todas las maquinas de la base de datos
    engine = sqlalchemy.create_engine("sqlite:///maquinas.db")
    with engine.connect() as connection:
        result = connection.execute(sqlalchemy.text('''
            SELECT nombre FROM maquinas
        '''))
        return [row[0] for row in result.fetchall()] #devuelve una lista con los nombres de las maquinas
#test
if __name__ == "__main__":
    crear_db() #ok
    #agregar_maquina("freza", "Operativo", "T-1000", "MarcaX", 5000.00) #ok ,agrega otra maquina igual si corre varias veces
    #agregar_incidente(2, "2024-06-01", "Resuelto", "Falla en el motor", 200.00, 4) #ok
    #eliminar_maquina(1) #ok ,elimina la maquina con id 1
    print(obtener_maquinas()) #ok ,muestra todas las maquinas en la base de datos
    print("listo") 
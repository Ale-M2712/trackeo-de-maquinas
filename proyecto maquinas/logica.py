import comandos_db as cdb
import pandas as pd
    
if __name__ == "__main__": #base de datos de prueba
    cdb.crear_db()
    cdb.agregar_maquina("Torno", "Operativo", "T-1000", "MarcaX", 5000.00)
    cdb.agregar_maquina("Fresa", "Operativo", "F-2000", "MarcaY", 7000.00)
    cdb.agregar_maquina("Taladro", "Operativo", "T-3000", "MarcaZ", 3000.00)
    cdb.agregar_maquina("sopladora", "Operativo", "S-4000", "MarcaW", 4000.00)
    cdb.agregar_maquina("Prensa", "Operativo", "P-5000", "MarcaV", 6000.00)
    cdb.agregar_maquina("Cortadora", "Operativo", "C-6000", "MarcaU", 8000.00)
    print("máquinas agregadas correctamente")

    print(pd.DataFrame(cdb.mostrar_tabla(), columns=["id", "nombre", "estado", "modelo", "marca", "costo"]))

    cdb.agregar_incidente(1, "2024-06-01 10:00:00", "Resuelto", "Falla en el motor", 200.00, 4)
    cdb.agregar_incidente(2, "2024-06-02 14:30:00", "Resuelto", "Problema eléctrico", 150.00, 2)
    cdb.agregar_incidente(3, "2024-06-03 09:15:00", "Resuelto", "Desgaste de piezas", 300.00, 6)
    cdb.agregar_incidente(4, "2024-06-04 16:45:00", "Resuelto", "Falla en el sistema de refrigeración", 250.00, 3)
    cdb.agregar_incidente(5, "2024-06-05 11:20:00", "Resuelto", "Problema de software", 100.00, 1)
    cdb.agregar_incidente(1, "2024-06-06 13:00:00", "Resuelto", "Falla en el motor nuevamente", 250.00, 5)
    cdb.agregar_incidente(1, "2024-06-07 15:30:00", "Resuelto", "Problema eléctrico", 150.00, 2)
    cdb.agregar_incidente(1, "2024-06-08 10:45:00", "Resuelto", "Desgaste de piezas", 300.00, 6)
    cdb.agregar_incidente(1, "2024-06-09 17:20:00", "Resuelto", "Falla en el sistema de refrigeración", 250.00, 3)
    print("incidentes agregados correctamente")

    print(pd.DataFrame(cdb.obtener_incidentes(1), columns=["id", "maquina_id", "fecha", "estado", "descripcion", "costos", "tiempo_de_parada"]))
   
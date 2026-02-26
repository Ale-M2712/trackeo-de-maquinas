import comandos_db as cdb

    
if __name__ == "__main__": #base de datos de prueba
    cdb.crear_db()
    cdb.agregar_maquina("Torno", "Operativo", "T-1000", "MarcaX", 5000.00)
    cdb.agregar_maquina("Fresa", "Operativo", "F-2000", "MarcaY", 7000.00)
    cdb.agregar_maquina("Taladro", "Operativo", "T-3000", "MarcaZ", 3000.00)
    cdb.agregar_maquina("sopladora", "Operativo", "S-4000", "MarcaW", 4000.00)
    cdb.agregar_maquina("Prensa", "Operativo", "P-5000", "MarcaV", 6000.00)
    cdb.agregar_maquina("Cortadora", "Operativo", "C-6000", "MarcaU", 8000.00)
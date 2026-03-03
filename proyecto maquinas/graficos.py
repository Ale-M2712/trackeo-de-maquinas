import matplotlib.pyplot as plt
import comandos_db as cdb
import numpy as np
import pandas as pd
import datetime

def preparar_datos(id_maquina):
    maquina = cdb.extraer_segun_id(id_maquina, "nombre")
    datos = cdb.obtener_incidentes(id_maquina)
    return pd.DataFrame(datos, columns=["id", "maquina_id", "fecha", "estado", "descripcion", "costos", "tiempo_de_parada"])

def incidentes_fecha(df):
    df2 = pd.to_datetime(df["fecha"]),df["tiempo_de_parada"]
    return df2

def graficos_incidentes(df):#tomamos el df2
    df2 = incidentes_fecha(df)
    plt.figure(figsize=(10, 6))

    # scatter: eje X=fecha, eje Y=tiempo_de_parada
    plt.scatter(
        df2["fecha"],
        df2["tiempo_de_parada"],
        c="blue",          # color de los puntos
        alpha=0.6,         # transparencia
        edgecolors="w",
        s=100,             # tamaño de los marcadores
    )

    plt.title(f"Incidentes máquina {df2['maquina_id'].iloc[0]}")
    plt.xlabel("Fecha")
    plt.ylabel("Tiempo de parada (horas)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()        
    plt.show()
    
if __name__ == "__main__":
    print(preparar_datos(1))
    print(incidentes_fecha(preparar_datos(1)))
    graficos_incidentes(preparar_datos(1))
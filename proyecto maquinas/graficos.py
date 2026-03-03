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

def graficos_incidentes(df):
    """Recibe un DataFrame de incidentes y devuelve la figura de matplotlib.

    El DataFrame se espera con al menos las columnas
    ``fecha``, ``maquina_id`` y ``tiempo_de_parada``. La columna ``fecha``
    se convierte a datetime para el eje x.
    """
    # aseguramos un dataframe local y convertimos la fecha
    df2 = df.copy()
    df2["fecha"] = pd.to_datetime(df2["fecha"])

    # creamos figura y ejes con el tamaño deseado
    fig, ax = plt.subplots(figsize=(10, 6))

    # scatter: eje X=fecha, eje Y=tiempo_de_parada
    ax.scatter(
        df2["fecha"],
        df2["tiempo_de_parada"],
        c="blue",          # color de los puntos
        alpha=0.6,         # transparencia
        edgecolors="w",
        s=100,             # tamaño de los marcadores
    )

    ax.set_title(f"Incidentes máquina {df2['maquina_id'].iloc[0]}")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Tiempo de parada (horas)")
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()

    # devolvemos la figura para que el llamador pueda manipular o mostrarla
    return fig

if __name__ == "__main__":
    print(preparar_datos(1))
    print(incidentes_fecha(preparar_datos(1)))
    print(graficos_incidentes(preparar_datos(1)))
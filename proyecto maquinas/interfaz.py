import sys
from pathlib import Path
import comandos_db as cdb
from PyQt6 import QtWidgets ,QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtGui import QPixmap
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import graficos

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interfaz de Usuario")
        self.resize(800, 600)

        # Layout principal (horizontal)
        self.layout_principal = QHBoxLayout()

        # --- Menú izquierdo ---
        self.layout_izquierdo = QVBoxLayout()

        self.selecion_maquinas = QVBoxLayout()

        #agregar y eliminar maquinas
        self.agregar_y_eliminar = QVBoxLayout()
        self.boton_agregar = QPushButton("Agregar Máquina")
        self.boton_agregar.setStyleSheet("""
            QPushButton {
                background-color: green;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: darkgreen;
            }
        """)
        self.boton_eliminar = QPushButton("Eliminar Máquina")
        self.boton_eliminar.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        self.agregar_y_eliminar.setStyleSheet("background-color: lightgray; padding: 10px;")

        self.agregar_y_eliminar.addWidget(self.boton_agregar)
        self.agregar_y_eliminar.addWidget(self.boton_eliminar)
        
        self.agregar_y_eliminar.addStretch(0)  # Espacio flexible para separar los botones de la lista el orden importa

        # --- Panel derecho ---
        self.layout_derecho = QVBoxLayout()
        self.label_derecho = QLabel("Selecciona una máquina")
        self.layout_derecho.addWidget(self.label_derecho)

        # Agregar los layouts al layout principal
        self.layout_principal.addLayout(self.layout_izquierdo, stretch=1)
        self.layout_principal.addLayout(self.layout_derecho, stretch=4)

        self.layout_izquierdo.addLayout(self.agregar_y_eliminar,stretch=1)
        self.layout_izquierdo.addLayout(self.selecion_maquinas,stretch=20)
        

        self.setLayout(self.layout_principal)

    def showEvent(self, event):
        super().showEvent(event)
        # Poblar los botones cuando la ventana ya tiene tamaño válido
        self.lista_maquinas()

    def lista_maquinas(self):
        # Limpiar el layout izquierdo antes de rellenar
        while self.selecion_maquinas.count():
            item = self.selecion_maquinas.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Obtener lista de máquinas desde la base
        lista = cdb.obtener_maquinas()

        for maquina in lista:
            boton = QPushButton(cdb.extraer_segun_id(maquina, "nombre"))
            # Botones expansivos en ancho, altura fija
            boton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            boton.setMinimumHeight(40)

            # Estilo visual
            boton.setStyleSheet("""
                QPushButton {
                    background-color: steelblue;
                    color: white;
                    font-weight: bold;
                    border-radius: 5px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: dodgerblue;
                }
            """)

            # Conectar acción → actualizar panel derecho
            boton.clicked.connect(lambda _, m=maquina: self.mostrar_maquina(m))
            self.selecion_maquinas.addWidget(boton)

    def mostrar_maquina(self, nombre):
        # Limpiar panel derecho
        while self.layout_derecho.count():
            item = self.layout_derecho.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Mostrar detalles de la máquina seleccionada
        label = QLabel(f"Detalles de {cdb.extraer_segun_id(nombre, 'nombre')}")
        label.setStyleSheet("font-size: 16px; background-color: lightyellow; padding: 10px; color:black;")
        self.layout_derecho.addWidget(label)
        ruta_imagen = Path(cdb.acceder_a_img(nombre))

        label_foto = QLabel()
        label_foto.setStyleSheet("background-color: lightyellow;")

        
        if ruta_imagen.exists():
            pixmap = QPixmap(str(ruta_imagen))
            # escalar la imagen para que no se desborde
            pixmap = pixmap.scaledToWidth(300)
            label_foto.setPixmap(pixmap)
            label_foto.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        else:
            label_foto.setText("Imagen no encontrada")

        self.layout_derecho.addWidget(label_foto)

        canvas = FigureCanvas(graficos.graficos_incidentes(graficos.preparar_datos(nombre)))
        self.layout_derecho.addWidget(canvas)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
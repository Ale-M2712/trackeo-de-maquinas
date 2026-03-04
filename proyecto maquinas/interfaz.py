import sys
from pathlib import Path
import comandos_db as cdb
from PyQt6 import QtWidgets ,QtCore
from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy, QDialog
from PyQt6.QtGui import QPixmap
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import graficos
import pandas as pd

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interfaz de Usuario")
        self.resize(800, 600)

        # Layout principal (horizontal)
        self.layout_primigenio = QHBoxLayout()
        contenedor_principal = QWidget() #con esto le doy color al fondo de la ventana
        contenedor_principal.setStyleSheet("background-color: white;")
        self.layout_principal = QHBoxLayout()
        contenedor_principal.setLayout(self.layout_principal)

        # --- Menú izquierdo ---
        contenedor = QWidget() #con esto le doy color al menu izquierdo
        contenedor.setStyleSheet("background-color: lightgray;")

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
        self.boton_agregar.clicked.connect(self.dialogo_agregar_maquina) #actualiza la lista de maquinas al agregar una nueva

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
        self.boton_eliminar.clicked.connect(self.dialogo_eliminar_maquina) #abre un dialogo para eliminar una maquina

        self.agregar_y_eliminar.addWidget(self.boton_agregar)
        self.agregar_y_eliminar.addWidget(self.boton_eliminar)
        
        self.agregar_y_eliminar.addStretch(0)  # Espacio flexible para separar los botones de la lista el orden importa

        contenedor.setLayout(self.layout_izquierdo)
        # --- Panel derecho ---
        contenedor_derecho = QWidget() #con esto le doy color al menu derecho
        contenedor_derecho.setStyleSheet("background-color: lightyellow;")
        self.layout_derecho = QVBoxLayout()
        self.label_derecho = QLabel("Selecciona una máquina")
        self.layout_derecho.addWidget(self.label_derecho)
        contenedor_derecho.setLayout(self.layout_derecho)

        # Agregar los layouts al layout principal
        self.layout_principal.addWidget(contenedor, stretch=1)
        self.layout_principal.addWidget(contenedor_derecho, stretch=4)

        self.layout_izquierdo.addLayout(self.agregar_y_eliminar,stretch=1)
        self.layout_izquierdo.addLayout(self.selecion_maquinas,stretch=20)
        

        self.layout_primigenio.addWidget(contenedor_principal)
        self.setLayout(self.layout_primigenio)
    def dialogo_agregar_maquina(self): #funciona ,solo tengo que mejorar el estilo
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Agregar Máquina")
        dialogo.resize(300, 200)

        # contenedor con fondo para todo el contenido del diálogo
        contenedor_dialogo = QWidget()
        contenedor_dialogo.setStyleSheet("background-color: white;")
        layout = QVBoxLayout(contenedor_dialogo)

        label = QLabel("Ingrese los detalles de la nueva máquina:")
        layout.addWidget(label)

        nombre_label = QLabel("Nombre:")
        nombre_label.setStyleSheet("color: black; font-weight: bold;")
        nombre_input = QLineEdit()
        nombre_input.setPlaceholderText("Nombre")
        nombre_input.setStyleSheet("background-color: lightgray;")

        label_estado = QLabel("Estado:")
        label_estado.setStyleSheet("color: black; font-weight: bold;")
        combo_estado = QtWidgets.QComboBox()
        combo_estado.addItems(["Operativa", "En reparación", "Fuera de servicio"])
        combo_estado.setStyleSheet("background-color: lightgray;")

        label_modelo = QLabel("Modelo:")
        label_modelo.setStyleSheet("color: black; font-weight: bold;")
        modelo_input = QLineEdit()
        modelo_input.setPlaceholderText("Modelo")
        modelo_input.setStyleSheet("background-color: lightgray;")

        label_marca = QLabel("Marca:")
        label_marca.setStyleSheet("color: black; font-weight: bold;")
        marca_input = QLineEdit()
        marca_input.setPlaceholderText("Marca")
        marca_input.setStyleSheet("background-color: lightgray;")

        label_costo = QLabel("Costo:")
        label_costo.setStyleSheet("color: black; font-weight: bold;")
        costo_input = QLineEdit()
        costo_input.setPlaceholderText("Costo")
        costo_input.setStyleSheet("background-color: lightgray;")

        layout.addWidget(nombre_label)
        layout.addWidget(nombre_input)
        layout.addWidget(label_estado)
        layout.addWidget(combo_estado)
        layout.addWidget(label_modelo)
        layout.addWidget(modelo_input)
        layout.addWidget(label_marca)
        layout.addWidget(marca_input)
        layout.addWidget(label_costo)
        layout.addWidget(costo_input)

        boton_guardar = QPushButton("Guardar")
        layout.addWidget(boton_guardar)

        # función interna para procesar y guardar los datos
        def guardar():
            nombre = nombre_input.text().strip()
            estado = combo_estado.currentText()
            modelo = modelo_input.text().strip()
            marca = marca_input.text().strip()
            costo_text = costo_input.text().strip()
            try:
                costo = float(costo_text) if costo_text else 0.0
            except ValueError:
                costo = 0.0

            if nombre:
                cdb.agregar_maquina(nombre, estado, modelo, marca, costo)
                dialogo.accept()
                self.lista_maquinas()
            else:
                # podría mostrar mensaje de error aquí
                pass

        boton_guardar.clicked.connect(guardar)

        # asigno el layout principal al diálogo
        layout_principal = QVBoxLayout()
        layout_principal.addWidget(contenedor_dialogo)
        dialogo.setLayout(layout_principal)

        dialogo.exec()
    def dialogo_eliminar_maquina(self): #funciona
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Eliminar Máquina")
        dialogo.resize(300, 150)
        layout = QVBoxLayout()
        label = QLabel("Ingrese el ID de la máquina a eliminar:")
        combo_maquinas = QtWidgets.QComboBox()
        maquinas = pd.DataFrame(cdb.tabla_maquinas())
        cdb.mostrar_tabla()#esto es solo para ver
        for maquina in maquinas.itertuples(index=False):
            maquina_id = maquina[0]# asumiendo que el ID está en la primera columna
            maquina_nombre = f"{maquina[1]}   {maquina[3]}"# asumiendo que el nombre está en la segunda columna
            combo_maquinas.addItem(maquina_nombre,maquina_id)#no esta agregando a la lista
        boton_eliminar = QPushButton("Eliminar")
        boton_eliminar.clicked.connect(lambda: cdb.eliminar_maquina(combo_maquinas.currentData())) #elimina la maquina seleccionada en el combo box
        layout.addWidget(label)
        layout.addWidget(combo_maquinas)
        layout.addWidget(boton_eliminar)

        dialogo.setLayout(layout)
        dialogo.exec()
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
import sys
import comandos_db as cdb
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton ,QSizePolicy

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interfaz de Usuario")

        # Layout principal (horizontal)
        self.layout = QHBoxLayout() 

        # --- Menú izquierdo ---
        self.layout_izquierdo = QVBoxLayout() #qvboxlayout es un layout vertical ,si fuera qhboxlayout seria horizontal
        
    
        # --- Menú derecho ---
        self.layout_derecho = QVBoxLayout() 
        label_derecho = QLabel("Menú derecho")
        boton_derecho = QPushButton("Botón derecho")
        boton_derecho.clicked.connect(lambda: print("Botón derecho clickeado"))
        self.layout_derecho.addWidget(label_derecho)
        self.layout_derecho.addWidget(boton_derecho)

        # Agregar los layouts al layout principal
        
        self.layout.addLayout(self.layout_izquierdo, stretch=1) #el orden de declaracion importa,se declara de izq a der
        self.layout.addLayout(self.layout_derecho, stretch=4)

        self.setLayout(self.layout)
        self.lista_maquinas() #llama a la funcion que muestra las maquinas en el menu izquierdo
    def lista_maquinas(self):
        lista = cdb.obtener_maquinas() #obtiene la lista de maquinas de la base de datos
        for maquina in lista:
            boton = QPushButton(maquina)
            boton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            boton.setMinimumHeight(int(self.height() * 0.3))
            boton.setStyleSheet("background-color: lightblue; color: black;")
            boton.clicked.connect(lambda _, m=maquina: print(f"Botón de {m} clickeado"))
            self.layout_izquierdo.addWidget(boton)
if __name__ == "__main__": #solo se ejecuta si corro este archivo
    app = QtWidgets.QApplication(sys.argv) #crea la aplicacion
    window = MainWindow() #crea la ventana que es un objeto de la clase MainWindow
    window.show() #muestra la ventana
    sys.exit(app.exec()) #asegura que la aplicacion se cierre correctamente al salir de la ventana
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
        self.layout_derecho.addWidget(label_derecho)
        

        # Agregar los layouts al layout principal
        
        self.layout.addLayout(self.layout_izquierdo, stretch=1) #el orden de declaracion importa,se declara de izq a der
        self.layout.addLayout(self.layout_derecho, stretch=4)

        self.setLayout(self.layout)
        # la lista de máquinas se poblará cuando la ventana se muestre
        # mediante showEvent para que tenga un tamaño válido

    def showEvent(self, event):
        super().showEvent(event)
        # ahora la geometría es correcta, rellenar los botones
        self.lista_maquinas()

    def lista_maquinas(self):
        # vaciar el layout izquierdo antes de rellenar
        while self.layout_izquierdo.count():
            item = self.layout_izquierdo.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        lista = cdb.obtener_maquinas() #obtiene la lista de maquinas de la base de datos
        for maquina in lista:
            boton = QPushButton(maquina)
            # permitir que cada botón se expanda verticalmente para ocupar el espacio disponible
            boton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            boton.setStyleSheet("""
        QPushButton {
            background-color: steelblue;
            color: white;
            font-weight: bold;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: dodgerblue;
        }
    """)

            boton.clicked.connect(lambda _, m=maquina: print(f"Botón de {m} clickeado"))
            self.layout_izquierdo.addWidget(boton)


            
if __name__ == "__main__": #solo se ejecuta si corro este archivo
    app = QtWidgets.QApplication(sys.argv) #crea la aplicacion
    window = MainWindow() #crea la ventana que es un objeto de la clase MainWindow
    window.show() #muestra la ventana
    sys.exit(app.exec()) #asegura que la aplicacion se cierre correctamente al salir de la ventana
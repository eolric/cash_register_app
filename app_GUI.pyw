import sys
from cash_register_GUI import *
from app import *  # Asegúrate de que este archivo está en el mismo directorio que app.py

# def createConnection():
#     """Crea una conexión a la base de datos SQLite"""
#     db = sqlite3.connect(db_file)
#     return True



class MiRegisradora(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)  # Llamada correcta al constructor padre
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Aquí puedes añadir tus conexiones de señales y slots
        # Ejemplo: self.ui.bt_cerrar.clicked.connect(self.close)
        #control-barra.de.titulos
        # Conexiones de señales y slots (accediendo a los botones a través de self.ui)
        self.ui.bt_minimizar.clicked.connect(self.control_bt_minimizar)
        self.ui.bt_restaurar.clicked.connect(self.control_bt_normal)
        self.ui.bt_maximizar.clicked.connect(self.control_bt_maximizar)
        self.ui.bt_cerrar.clicked.connect(lambda: self.close())

    def control_bt_minimizar(self):
        self.showMinimized()

    def control_bt_normal(self):
        self.showNormal()
        self.ui.bt_restaurar.hide()
        self.ui.bt_maximizar.show()

    def control_bt_maximizar(self):
        self.showMaximized()
        self.ui.bt_maximizar.hide()
        self.ui.bt_restaurar.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MiRegisradora()
    myapp.show()
    sys.exit(app.exec_())


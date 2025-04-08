import sys
from cash_register_GUI import *

class MiRegisradora(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)  # Llamada correcta al constructor padre
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Aquí puedes añadir tus conexiones de señales y slots
        # Ejemplo: self.ui.bt_cerrar.clicked.connect(self.close)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MiRegisradora()
    myapp.show()
    sys.exit(app.exec_())


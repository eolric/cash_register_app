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
        #Botones de control de ventana
        self.ui.bt_minimizar.clicked.connect(self.control_bt_minimizar)
        self.ui.bt_restaurar.clicked.connect(self.control_bt_normal)
        self.ui.bt_maximizar.clicked.connect(self.control_bt_maximizar)
        self.ui.bt_cerrar.clicked.connect(lambda: self.close())

         # Configuración del SizeGrip - Ventana
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)
        
        # Para mover la ventana (debe aplicarse al frame superior)
        self.ui.frame_sup.mouseMoveEvent = self.mover_ventana
        self.ui.frame_sup.mousePressEvent = self.mouse_press_event

        #botones de la barra de control
        # Configuración inicial para mostrar la página correcta al cambiar sección
        self.ui.bt_baseDatos.clicked.connect(self.show_database_section)
        self.ui.bt_ventas.clicked.connect(self.show_sales_section)
        self.ui.bt_reportes.clicked.connect(self.show_reports_section)

        #botones de control de submenus
        #Productos
        self.ui.bt_ver.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_ver))
        self.ui.bt_add.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_add))
        self.ui.bt_delete.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_delete))
        self.ui.bt_update.clicked.connect(self.control_bt_update)
        self.ui.bt_search.clicked.connect(self.control_bt_search)


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

    def mouse_press_event(self, event):
        self.old_pos = event.globalPos()

    def mover_ventana(self, event):
        if hasattr(self, 'old_pos'):
            delta = QtCore.QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def control_bt_menu(self):
        pass

    def show_database_section(self):
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_subDB)
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_ver)  # Mostrar página inicial de DB

    def show_sales_section(self):
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_subVentas)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_newSale)

    def show_reports_section(self):
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_subReports)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_exportReport)

    def control_bt_ver(self):
        pass

    def control_bt_add(self):
        pass    

    def control_bt_delete(self):
        pass

    def control_bt_update(self):
        pass

    def control_bt_search(self):
        pass




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MiRegisradora()
    myapp.show()
    sys.exit(app.exec_())


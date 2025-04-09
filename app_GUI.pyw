import sys
from cash_register_GUI import *
from datetime import datetime
from models.product_model import Producto
from models.sale_model import Venta
from services.database_service import (
    crear_conexion,
    verificar_tablas,
    insertar_producto,
    obtener_productos,
    registrar_venta,
    obtener_detalle_venta,
    actualizar_inventario,
    consultar_ventas_por_fecha,
    exportar_reporte_csv,
    eliminar_producto,
    buscar_productos
)# Asegúrate de que este archivo está en el mismo directorio que app.py

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
        self.ui.bt_menu.clicked.connect(self.control_bt_menu)
        # Configuración inicial para mostrar la página correcta al cambiar sección
        self.ui.bt_baseDatos.clicked.connect(self.show_database_section)
        self.ui.bt_ventas.clicked.connect(self.show_sales_section)
        self.ui.bt_reportes.clicked.connect(self.show_reports_section)

        #botones de control de submenus
        #Productos
        self.ui.bt_ver.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_ver))
        self.ui.bt_add.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_add))
        self.ui.bt_delete.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_delete))
        self.ui.bt_update.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_update))
        self.ui.bt_search.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_search))

        #Ventas
        self.ui.bt_newSale.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_newSale))
        self.ui.bt_salesSearch.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_saleSearch))

        #Reportes
        self.ui.bt_exportReport.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_exportReport))

        #ajuste de table Widget a la ventana
        self.ui.tableWidget_pgSearch.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget_produc_pgVer.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget_pgSearchSale.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget_pgDelet.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        #botones de acción
        self.ui.bt_refrescar_pgVer.clicked.connect(self.control_bt_refrescar_pgVer)
        self.ui.bt_add_pgAdd.clicked.connect(self.control_bt_add_pgAdd)
        self.ui.bt_buscar_pgDelet.clicked.connect(self.contro_bt_buscar_pgDelet)
        self.ui.bt_delete_pgDelete.clicked.connect(self.control_bt_delete_pgDelete)
        self.ui.bt_update_pgUpdate.clicked.connect(self.control_bt_update_pgUpdate)
        self.ui.bt_buscar_pgSearch.clicked.connect(self.control_bt_buscar_pgSearch)

        self.ui.bt_add_pgRegisterSale.clicked.connect(self.control_bt_add_pgRegisterSale)
        self.ui.bt_finish_pgRegisterSale.clicked.connect(self.control_bt_finish_pgRegisterSale)
        self.ui.bt_search_pgSearchSale.clicked.connect(self.control_bt_search_pgSearchSale)

        self.ui.bt_download_pgReport.clicked.connect(self.control_bt_download_pgReport)
        


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

    # Para mover el menu lateral izquierdo
    def control_bt_menu(self):
        if True:
            width = self.ui.frame_control.width()
            normal = 0
        if width==0:
            extender = 200
        else:
            extender = normal
        self.animacion = QtCore.QPropertyAnimation(self.ui.frame_control, b'minimumWidth')
        self.animacion.setDuration(300)
        self.animacion.setStartValue(width)
        self.animacion.setEndValue(extender)
        self.animacion.setEasingCurve (QtCore.QEasingCurve. InOutQuart)
        self.animacion.start()

    def show_database_section(self):
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_subDB)
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_ver)  # Mostrar página inicial de DB

    def show_sales_section(self):
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_subVentas)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_newSale)

    def show_reports_section(self):
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_subReports)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_exportReport)

    def control_bt_refrescar_pgVer(self):
        conn = crear_conexion()
        print("\n--- LISTA DE PRODUCTOS ---")
        productos = obtener_productos(conn)
        if not productos:
            print("No hay productos registrados")
            return
        i = len(productos)
        self.ui.tableWidget_produc_pgVer.setRowCount(i)
        table_row = 0
        for row in productos:
            self.ui.tableWidget_produc_pgVer.setItem(table_row, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.ui.tableWidget_produc_pgVer.setItem(table_row, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.ui.tableWidget_produc_pgVer.setItem(table_row, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.ui.tableWidget_produc_pgVer.setItem(table_row, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.ui.tableWidget_produc_pgVer.setItem(table_row, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            table_row += 1

    def control_bt_add_pgAdd(self):
        conn = crear_conexion()
        print("\n--- AGREGAR PRODUCTO ---")
        try:
            codigo = self.ui.lineEdit_cod_pgAdd.text()
            nombre = self.ui.lineEdit_name_pgAdd.text()
            cantidad = int(self.ui.lineEdit_cnt_pgAdd.text())
            # precio_compra = float(input("Precio de compra unitario: "))
            # precio_venta = float(input("Precio de venta unitario: "))
            
            # producto = Producto(codigo, nombre, cantidad, precio_compra, precio_venta)
            # insertar_producto(conn, producto)
        except ValueError:
            print("Error: Asegúrese de ingresar valores numéricos para cantidad y precios")
            QtWidgets.QMessageBox.warning(self, "Error", "¡El campo no puede estar vacío!")

    def contro_bt_buscar_pgDelet(self):
        pass

    def control_bt_delete_pgDelete(self):
        pass

    def control_bt_update_pgUpdate(self):
        pass

    def control_bt_buscar_pgSearch(self):
        pass

    def control_bt_add_pgRegisterSale(self):
        pass

    def control_bt_finish_pgRegisterSale(self):
        pass

    def control_bt_search_pgSearchSale(self):
        pass

    def control_bt_download_pgReport(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    conn = crear_conexion()
    if conn is not None:
        verificar_tablas(conn)
    else:
        print("Error! No se puede conectar a la base de datos")
        sys.exit(1)
    myapp = MiRegisradora()
    myapp.show()
    sys.exit(app.exec_())


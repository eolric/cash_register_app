import sys
from cash_register_GUI import *
from datetime import datetime
from models.product_model import Producto
from models.sale_model import Venta
from models.carrito_model import CarritoCompras
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
        
        self.carrito = CarritoCompras()  # Instancia del carrito
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
            codigo = self.ui.lineEdit_cod_pgAdd.text().rstrip()
            nombre = self.ui.lineEdit_name_pgAdd.text().rstrip()
            cantidad = int(self.ui.lineEdit_cnt_pgAdd.text().rstrip())
            precio_compra = float(self.ui.lineEdit_preComp_pgAdd.text().rstrip())
            precio_venta = float(self.ui.lineEdit_preVenta_pgAdd.text().rstrip())

            # Verificar si el código ya existe
            cursor = conn.cursor()
            cursor.execute("SELECT codigo FROM productos WHERE codigo = ?", (codigo,))
            if cursor.fetchone() is not None:
                self.ui.label_pgAdd.setText("El producto ya existe, verifique el código")
                self.ui.label_pgAdd.setStyleSheet("color: red;")
                return
        
            producto = Producto(codigo, nombre, cantidad, precio_compra, precio_venta)
            
            if insertar_producto(conn, producto):
                self.ui.label_pgAdd.setText("Producto agregado exitosamente")
                self.ui.label_pgAdd.setStyleSheet("color: green;")
                # Limpiar los campos después de agregar
                self.ui.lineEdit_cod_pgAdd.clear()
                self.ui.lineEdit_name_pgAdd.clear()
                self.ui.lineEdit_cnt_pgAdd.clear()
                self.ui.lineEdit_preComp_pgAdd.clear()
                self.ui.lineEdit_preVenta_pgAdd.clear()

        except ValueError as e:
            print(f"Error: {e}")
            self.ui.label_pgAdd.setText("Error: Verifique los datos ingresados")
            self.ui.label_pgAdd.setStyleSheet("color: red;")
            QtWidgets.QMessageBox.warning(self, "Error", "¡Debe ingresar valores válidos!\nLos campos no pueden estar en blanco\nCantidad y precios deben ser números")

    def contro_bt_buscar_pgDelet(self):
        conn = crear_conexion()
        try:
            codigo = self.ui.lineEdit_cod_pgDelet.text().rstrip()
        # Verificar si el código ya existe
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos WHERE codigo = ?", (codigo,))
            producto = cursor.fetchone()
            if not producto:
                self.ui.label_pgDelet.setText("El producto no existe, verifique el código")
                self.ui.label_pgDelet.setStyleSheet("color: red;")
                return 
            else:
                self.ui.tableWidget_pgDelet.setRowCount(1)
                self.ui.tableWidget_pgDelet.setItem(0, 0, QtWidgets.QTableWidgetItem(str(producto[0])))
                self.ui.tableWidget_pgDelet.setItem(0, 1, QtWidgets.QTableWidgetItem(str(producto[1])))
                self.ui.tableWidget_pgDelet.setItem(0, 2, QtWidgets.QTableWidgetItem(str(producto[2])))
                self.ui.tableWidget_pgDelet.setItem(0, 3, QtWidgets.QTableWidgetItem(str(producto[3])))
                self.ui.tableWidget_pgDelet.setItem(0, 4, QtWidgets.QTableWidgetItem(str(producto[4])))
                self.ui.label_pgDelet.setText("")
        except ValueError as e:
            print(f"Error: {e}")
            

    def control_bt_delete_pgDelete(self):
        conn = crear_conexion()
        try:
            codigo = self.ui.lineEdit_cod_pgDelet.text().rstrip()
            if not codigo:
                self.ui.label_pgDelet.setText("Debe de ingresar un código válido")
                self.ui.label_pgDelet.setStyleSheet("color: red;")
                return
        # Mostrar diálogo de confirmación
            respuesta = QtWidgets.QMessageBox.question(
                self,
                "Confirmar eliminación",
                f"¿Está seguro de eliminar el producto (Código: {codigo})?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No  # Botón por defecto
            )
            if respuesta == QtWidgets.QMessageBox.Yes:
                if eliminar_producto(conn, codigo):
                    self.ui.label_pgDelet.setText("Éxito, producto eliminado correctamente")
                    self.ui.label_pgDelet.setStyleSheet("color: green;")
                    # Limpiar campos después de eliminar
                    self.ui.lineEdit_cod_pgDelet.clear()
                    self.ui.tableWidget_pgDelet.setRowCount(0)  # Limpiar la tabla 
                else:
                    self.ui.label_pgDelet.setText("Error, no se pudo eliminar el producto")
                    self.ui.label_pgDelet.setStyleSheet("color: red;")
            self.ui.label_pgDelet.setText("")
        except ValueError as e:
            print(f"Error: {e}")
            self.ui.label_pgDelet.setText("Error: Verifique el código ingresado")
            self.ui.label_pgDelet.setStyleSheet("color: red;")
            
    def control_bt_update_pgUpdate(self):
        conn = crear_conexion()
        try:
            codigo = self.ui.lineEdit_cnt_pgUpdate.text().rstrip()
            cantidad = int(self.ui.lineEdit_cod_pgUpdate.text().rstrip())
            if actualizar_inventario(conn, codigo, cantidad):
                self.ui.label_pgUpdate.setText("Éxito, producto actualizado correctamente")
                self.ui.label_pgUpdate.setStyleSheet("color: green;")
                self.ui.lineEdit_cnt_pgUpdate.clear()
                self.ui.lineEdit_cod_pgUpdate.clear()
            else:
                self.ui.label_pgUpdate.setText("Error, producto no encontrado")
                self.ui.label_pgUpdate.setStyleSheet("color: red;")
        except ValueError as e:
            print(f"Error: {e}")
            self.ui.label_pgUpdate.setText("Error: Verifique los datos ingresados")
            self.ui.label_pgUpdate.setStyleSheet("color: red;")
            QtWidgets.QMessageBox.warning(self, "Error", "¡Debe ingresar valores válidos!\nLos campos no pueden estar en blanco\nCantidad debe ser un número positivo o negativo")
            return

    def control_bt_buscar_pgSearch(self):
        conn = crear_conexion()
        try:
            word_clave = self.ui.lineEdit_pgSearch.text().rstrip()
            if word_clave:
                productos = buscar_productos(conn, word_clave)
                i = len(productos)
                self.ui.tableWidget_pgSearch.setRowCount(i)
                table_row = 0
                for row in productos:
                    self.ui.tableWidget_pgSearch.setItem(table_row, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.ui.tableWidget_pgSearch.setItem(table_row, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    self.ui.tableWidget_pgSearch.setItem(table_row, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                    self.ui.tableWidget_pgSearch.setItem(table_row, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                    self.ui.tableWidget_pgSearch.setItem(table_row, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    table_row += 1
                self.ui.lineEdit_pgSearch.clear()   #Se limpia el campo de búsqueda 
            if not productos:
                self.ui.label_pgSearch.setText("No se encontró el producto")
                self.ui.label_pgSearch.setStyleSheet("color: red;")
                return
            self.ui.label_pgSearch.setText("")
        except ValueError as e:
            print(f"Error: {e}")
            self.ui.label_pgSearch.setText("¡Debe ingresar valores válidos!\nLos campos no pueden estar en blanco")
            self.ui.label_pgSearch.setStyleSheet("color: red;")
            return

    def control_bt_add_pgRegisterSale(self):
        conn = crear_conexion()
        try:
            codigo = self.ui.lineEdit_cod_pgRegisterSale.text().rstrip()
            cantidad_in = self.ui.lineEdit_cnt_pgRegisterSale.text().rstrip()
            descuento_in = self.ui.lineEdit_desc_pgRegisterSale.text().rstrip()
            vendedor = self.ui.lineEdit_vend_pgRegisterSale.text().rstrip()
            # Validaciones básicas
            if not codigo or not cantidad_in:
                self.ui.label_pgRegisterSale.setText("Código y cantidad son obligatorios")
                self.ui.label_pgRegisterSale.setStyleSheet("color: red;")
                return
            cantidad = int(cantidad_in)
            descuento = float(descuento_in) if descuento_in else 0.0
            
            # Verificar que el producto existe y tiene stock suficiente
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, cantidad, precio_venta FROM productos WHERE codigo = ?", (codigo,))
            producto = cursor.fetchone()
            
            if not producto:
                self.ui.label_pgRegisterSale.setText("Producto no encontrado")
                self.ui.label_pgRegisterSale.setStyleSheet("color: red;")
                return
                
            nombre_producto, stock_actual, precio_venta = producto
            
            if cantidad <= 0:
                self.ui.label_pgRegisterSale.setText("Cantidad debe ser positiva")
                self.ui.label_pgRegisterSale.setStyleSheet("color: red;")
                return
                
            if stock_actual < cantidad:
                self.ui.label_pgRegisterSale.setText(f"Stock insuficiente (Disponible: {stock_actual})")
                self.ui.label_pgRegisterSale.setStyleSheet("color: red;")
                return
                
            # Agregar al carrito
            subtotal = self.carrito.agregar_item(
                codigo, nombre_producto, cantidad, precio_venta, descuento, vendedor
            )
            
            # Mostrar información al usuario
            mensaje = f"Se agregó: {nombre_producto} al carrito de compras\nCant: {cantidad}\n${subtotal:.2f}"
            QtWidgets.QMessageBox.information(self, "Éxito", mensaje)
            
            # Limpiar campos (excepto vendedor)
            self.ui.lineEdit_cod_pgRegisterSale.clear()
            self.ui.lineEdit_cnt_pgRegisterSale.clear()
            self.ui.lineEdit_desc_pgRegisterSale.clear()
        
        except ValueError as e:
            print(f"Error: {e}")
            self.ui.label_pgRegisterSale.setText("Error: Verifique los datos ingresados")
            self.ui.label_pgRegisterSale.setStyleSheet("color: red;")
            QtWidgets.QMessageBox.warning(self, "Error", 
                                          "¡Debe ingresar valores válidos!\nCantidad debe ser número entero\nDescuento debe ser número")

    def control_bt_finish_pgRegisterSale(self):
        if not self.carrito.obtener_items():
            self.ui.label_pgRegisterSale.setText("No hay productos en la venta")
            self.ui.label_pgRegisterSale.setStyleSheet("color: red;")
            return
        
        try:
            efectivo = float(self.ui.lineEdit_efect_pgRegisterSale.text().strip())
            total = self.carrito.calcular_total()
            cambio = efectivo - total
            if efectivo < total:
                self.ui.label_pgRegisterSale.setText(f"Efectivo insuficiente. Total: ${total:.2f}")
                self.ui.label_pgRegisterSale.setStyleSheet("color: red;")
                return
            conn = crear_conexion()
            # Registrar ventas
            for item in self.carrito.obtener_items():
                venta = Venta(
                    item['codigo'],
                    item['cantidad'], 
                    item['descuento'],
                    item['vendedor']
                )
                if not registrar_venta(conn, venta):
                    QtWidgets.QMessageBox.critical(self, "Error", 
                                                   f"No se logro registrar la venta del producto {item['codigo']}")
            self.ui.label_pgRegisterSale.setText("Éxito: venta registrada correctamente")
            self.ui.label_pgRegisterSale.setStyleSheet("color: green;")
            QtWidgets.QMessageBox.information(self, "Éxito", "Cambio: ${:.2f}".format(cambio))
        
            # Limpiar
            self.carrito.vaciar()
            self.ui.lineEdit_cod_pgRegisterSale.clear()
            self.ui.lineEdit_cnt_pgRegisterSale.clear()
            self.ui.lineEdit_desc_pgRegisterSale.clear()
            self.ui.lineEdit_efect_pgRegisterSale.clear()
            self.ui.lineEdit_vend_pgRegisterSale.clear()

        except ValueError as e:
            print(f"Error: {e}")
            self.ui.label_pgRegisterSale.setText("Error: Verifique los datos ingresados")
            self.ui.label_pgRegisterSale.setStyleSheet("color: red;")
            QtWidgets.QMessageBox.warning(self, "Error", "¡Debe ingresar valores válidos!\nLos campos no pueden estar en blanco, debe ingresar una cantidad en efectivo")
            return

    def control_bt_search_pgSearchSale(self):
        conn = crear_conexion()
        try:
            fecha_inicio = self.ui.lineEdit_iniDate_pgSearchSale.text().strip()
            fecha_fin = self.ui.lineEdit_finDate_pgSearchSale.text().strip()
            
            if not fecha_inicio or not fecha_fin:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "Debe ingresar ambas fechas")
                return
            ventas = consultar_ventas_por_fecha(conn, fecha_inicio, fecha_fin)
            
            if not ventas:
                QtWidgets.QMessageBox.information(self, "Información", "No se encontraron ventas en ese rango de fechas")
                return
            # Mostrar resultados en la tabla
            self.ui.tableWidget_pgSearchSale.setRowCount(len(ventas))
            
            for row_idx, venta in enumerate(ventas):
                # Calcular subtotal
                subtotal = venta[3] * venta[4] * (1 - venta[5]/100)
                
                # Añadir datos a la tabla
                self.ui.tableWidget_pgSearchSale.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(venta[0]))  # Fecha
                self.ui.tableWidget_pgSearchSale.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(venta[1]))  # Hora
                self.ui.tableWidget_pgSearchSale.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(venta[2]))  # Producto
                self.ui.tableWidget_pgSearchSale.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(venta[3])))  # Cantidad
                self.ui.tableWidget_pgSearchSale.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(f"{venta[4]:.2f}"))  # Precio
                self.ui.tableWidget_pgSearchSale.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(f"{venta[5]:.2f}"))  # Descuento
                self.ui.tableWidget_pgSearchSale.setItem(row_idx, 6, QtWidgets.QTableWidgetItem(f"{subtotal:.2f}"))  # Subtotal
                self.ui.tableWidget_pgSearchSale.setItem(row_idx, 7, QtWidgets.QTableWidgetItem(venta[6]))  # Vendedor
                
        except Exception as e:
            print(f"Error al buscar ventas: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", "Ocurrió un error al buscar ventas")

    def control_bt_download_pgReport(self):
        conn = crear_conexion()
        try:
            fecha_inicio = self.ui.lineEdit_iniDate_pgReport.text().strip()
            fecha_fin = self.ui.lineEdit_finDate_pgReport.text().strip()
            nombre_doc = self.ui.lineEdit_nameDoc_pgReport.text().strip()
            
            if not fecha_inicio or not fecha_fin:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "Debe ingresar ambas fechas")
                return
                
            if not nombre_doc:
                nombre_doc = f"reporte_ventas_{fecha_inicio}_{fecha_fin}"
                
            # Definir la ruta donde se guardará el reporte
            # Abrir diálogo para seleccionar ubicación
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Guardar Reporte",
            f"{nombre_doc}.csv",  # Nombre sugerido
            "Archivos CSV (*.csv);;Todos los archivos (*)"
            )
            if not file_path:  # Usuario canceló
                return

            # Asegurar extensión .csv
            if not file_path.lower().endswith('.csv'):
                file_path += '.csv'
                
            if exportar_reporte_csv(conn, fecha_inicio, fecha_fin, file_path):
                QtWidgets.QMessageBox.information(
                    self, 
                    "Éxito", 
                    f"Reporte generado exitosamente\nGuardado en: {file_path}"
                )
            else:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Advertencia", 
                    "No se pudo generar el reporte o no hay datos para el rango de fechas"
                )
                
        except Exception as e:
            print(f"Error al generar reporte: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", "Ocurrió un error al generar el reporte:\n{str(e)}")

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


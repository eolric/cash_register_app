import os
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
)
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi

class VentanaPrincipal (QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        loadUi('diseño.ui', self)
        self.bt_menu.clicked.connect(self.mover_menu)
        #clase comunicacion sqlite
        self.base_datos = Comunicacion ()
        #self.Id = str()
        # ocultamos los botones
        self.bt_restaurar.hide()
#botones

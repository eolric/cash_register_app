import sqlite3
import csv
from datetime import datetime
import os
from pathlib import Path
from services.config_service import cargar_configuracion, generar_sql_creacion_tabla

config = cargar_configuracion()
DB_PATH = Path(__file__).parent.parent / "database" / config['database_name']

def crear_conexion():
    """Crear una conexión a la base de datos SQLite"""
    conn = None
    try:
        # Crear directorio si no existe
        os.makedirs(DB_PATH.parent, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        print(f"Conexión a SQLite establecida ({DB_PATH})")
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a SQLite: {e}")
    return conn

def verificar_tablas(conn):
    """Verificar y crear todas las tablas según configuración"""
    for tabla in config['tables']:
        verificar_tabla(conn, tabla)

def verificar_tabla(conn, nombre_tabla):
    """Verificar y crear una tabla específica según configuración"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT count(name) FROM sqlite_master 
            WHERE type='table' AND name='{nombre_tabla}'
        """)
        if cursor.fetchone()[0] == 0:
            sql_creacion = generar_sql_creacion_tabla(nombre_tabla)
            if sql_creacion:
                cursor.execute(sql_creacion)
                conn.commit()
                print(f"Tabla '{nombre_tabla}' creada exitosamente")
            else:
                print(f"Error: No se encontró configuración para la tabla '{nombre_tabla}'")
        else:
            print(f"Tabla '{nombre_tabla}' ya existe")
    except sqlite3.Error as e:
        print(f"Error al verificar/crear tabla {nombre_tabla}: {e}")

def insertar_producto(conn, producto):
    """Insertar un nuevo producto en la base de datos"""
    sql = """
        INSERT INTO productos(codigo, nombre, cantidad, precio_compra, precio_venta)
        VALUES(?,?,?,?,?)
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (
            producto.codigo,
            producto.nombre,
            producto.cantidad,
            producto.precio_compra,
            producto.precio_venta
        ))
        conn.commit()
        print("Producto agregado exitosamente")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error al insertar producto: {e}")
        return None

def obtener_productos(conn):
    """Obtener todos los productos de la base de datos"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Error al obtener productos: {e}")
        return []

def eliminar_producto(conn, codigo):
    """Eliminar un producto de la base de datos"""
    try:
        cursor = conn.cursor()
        # Verificar si el producto existe
        cursor.execute("SELECT nombre FROM productos WHERE codigo = ?", (codigo,))
        producto = cursor.fetchone()
        
        if not producto:
            print("Producto no encontrado")
            return False
            
        # Eliminar el producto
        cursor.execute("DELETE FROM productos WHERE codigo = ?", (codigo,))
        conn.commit()
        print(f"Producto '{producto[0]}' eliminado exitosamente")
        return True
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error al eliminar producto: {e}")
        return False

def registrar_venta(conn, venta):
    """Registrar una venta y actualizar el stock"""
    try:
        # Verificar stock disponible
        cursor = conn.cursor()
        cursor.execute("SELECT cantidad FROM productos WHERE codigo = ?", (venta.codigo_producto,))
        resultado = cursor.fetchone()
        
        if not resultado:
            raise ValueError("Producto no encontrado")
        
        stock_actual = resultado[0]
        if stock_actual < venta.cantidad:
            raise ValueError("Stock insuficiente")
        
        # Actualizar stock
        nuevo_stock = stock_actual - venta.cantidad
        cursor.execute(
            "UPDATE productos SET cantidad = ? WHERE codigo = ?",
            (nuevo_stock, venta.codigo_producto)
        )
        
        # Registrar venta
        cursor.execute(
            """INSERT INTO ventas(fecha, hora, codigo_producto, cantidad, descuento, vendedor)
            VALUES(?,?,?,?,?,?)""",
            (venta.fecha, venta.hora, venta.codigo_producto, venta.cantidad, venta.descuento, venta.vendedor)
        )
        
        conn.commit()
        return True
    except (sqlite3.Error, ValueError) as e:
        conn.rollback()
        print(f"Error al registrar venta: {e}")
        return False

def obtener_detalle_venta(conn, codigo_producto):
    """Obtener detalles del producto para la venta"""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nombre, precio_venta FROM productos WHERE codigo = ?",
        (codigo_producto,)
    )
    return cursor.fetchone()

def actualizar_inventario(conn, codigo_producto, cantidad):
    """Actualizar la cantidad en inventario de un producto"""
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE productos SET cantidad = cantidad + ? WHERE codigo = ?",
            (cantidad, codigo_producto)
        )
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error al actualizar inventario: {e}")
        return False

def consultar_ventas_por_fecha(conn, fecha_inicio, fecha_fin):
    """Consultar ventas en un rango de fechas"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.fecha, v.hora, p.nombre, v.cantidad, p.precio_venta, v.descuento, v.vendedor
            FROM ventas v
            JOIN productos p ON v.codigo_producto = p.codigo
            WHERE v.fecha BETWEEN ? AND ?
            ORDER BY v.fecha, v.hora
        """, (fecha_inicio, fecha_fin))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al consultar ventas: {e}")
        return []

def exportar_reporte_csv(conn, fecha_inicio, fecha_fin, archivo_salida):
    """Exportar reporte de ventas a CSV"""
    ventas = consultar_ventas_por_fecha(conn, fecha_inicio, fecha_fin)
    if not ventas:
        return False
    
    try:
        with open(archivo_salida, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Fecha', 'Hora', 'Producto', 'Cantidad', 
                'Precio Unitario', 'Descuento %', 'Subtotal', 'Vendedor'
            ])
            
            for venta in ventas:
                subtotal = venta[3] * venta[4] * (1 - venta[5]/100)
                writer.writerow([
                    venta[0], venta[1], venta[2], venta[3],
                    f"{venta[4]:.2f}", f"{venta[5]:.2f}", f"{subtotal:.2f}", venta[6]
                ])
        return True
    except IOError as e:
        print(f"Error al exportar CSV: {e}")
        return False
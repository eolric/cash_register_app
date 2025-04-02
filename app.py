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

def mostrar_menu():
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Gestión de Productos")
    print("2. Gestión de Ventas")
    print("3. Reportes")
    print("4. Salir")

def menu_productos(conn):
    while True:
        print("\n--- GESTIÓN DE PRODUCTOS ---")
        print("1. Agregar nuevo producto")
        print("2. Ver todos los productos")
        print("3. Buscar productos")
        print("4. Actualizar inventario")
        print("5. Eliminar producto")
        print("6. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            agregar_producto(conn)
        elif opcion == "2":
            ver_productos(conn)
        elif opcion == "3":
            buscar_productos_interactivo(conn)
        elif opcion == "4":
            actualizar_inventario_interactivo(conn)
        elif opcion == "5":
            eliminar_producto_interactivo(conn)
        elif opcion == "6":
            break
        else:
            print("Opción no válida")

def agregar_producto(conn):
    print("\n--- AGREGAR PRODUCTO ---")
    try:
        codigo = input("Código del producto: ")
        nombre = input("Nombre: ")
        cantidad = int(input("Cantidad: "))
        precio_compra = float(input("Precio de compra unitario: "))
        precio_venta = float(input("Precio de venta unitario: "))
        
        producto = Producto(codigo, nombre, cantidad, precio_compra, precio_venta)
        insertar_producto(conn, producto)
    except ValueError:
        print("Error: Asegúrese de ingresar valores numéricos para cantidad y precios")

def ver_productos(conn):
    print("\n--- LISTA DE PRODUCTOS ---")
    productos = obtener_productos(conn)
    if not productos:
        print("No hay productos registrados")
        return
    
    print("{:<10} {:<20} {:<10} {:<15} {:<15}".format(
        "Código", "Nombre", "Cantidad", "P. Compra", "P. Venta"
    ))
    print("-" * 70)
    for prod in productos:
        print("{:<10} {:<20} {:<10} {:<15.2f} {:<15.2f}".format(
            prod[0], prod[1], prod[2], prod[3], prod[4]
        ))

def actualizar_inventario_interactivo(conn):
    print("\n--- ACTUALIZAR INVENTARIO ---")
    codigo = input("Código del producto: ")
    try:
        cantidad = int(input("Cantidad a agregar (use negativo para descontar): "))
        if actualizar_inventario(conn, codigo, cantidad):
            print("Inventario actualizado exitosamente")
        else:
            print("Producto no encontrado")
    except ValueError:
        print("Error: La cantidad debe ser un número entero")

def buscar_productos_interactivo(conn):
    print("\n--- BUSCAR PRODUCTOS ---")
    criterio = input("Ingrese código o palabra clave del nombre: ").strip()
    
    if not criterio:
        print("Debe ingresar un criterio de búsqueda")
        return
    
    productos = buscar_productos(conn, criterio)
    
    if not productos:
        print("No se encontraron productos con ese criterio")
        return
    
    print("\n--- RESULTADOS DE BÚSQUEDA ---")
    print("{:<10} {:<20} {:<10} {:<15} {:<15}".format(
        "Código", "Nombre", "Cantidad", "P. Compra", "P. Venta"
    ))
    print("-" * 70)
    for prod in productos:
        print("{:<10} {:<20} {:<10} {:<15.2f} {:<15.2f}".format(
            prod[0], prod[1], prod[2], prod[3], prod[4]
        ))

def eliminar_producto_interactivo(conn):
    print("\n--- ELIMINAR PRODUCTO ---")
    codigo = input("Ingrese el código del producto a eliminar: ")
    
    # Mostrar información del producto antes de eliminar
    productos = obtener_productos(conn)
    producto_a_eliminar = None
    
    for prod in productos:
        if prod[0] == codigo:
            producto_a_eliminar = prod
            break
    
    if producto_a_eliminar:
        print("\nProducto encontrado:")
        print(f"Código: {producto_a_eliminar[0]}")
        print(f"Nombre: {producto_a_eliminar[1]}")
        print(f"Cantidad: {producto_a_eliminar[2]}")
        print(f"Precio compra: {producto_a_eliminar[3]:.2f}")
        print(f"Precio venta: {producto_a_eliminar[4]:.2f}")
        
        confirmacion = input("\n¿Está seguro que desea eliminar este producto? (s/n): ").lower()
        if confirmacion == 's':
            if eliminar_producto(conn, codigo):
                print("Producto eliminado exitosamente")
            else:
                print("No se pudo eliminar el producto")
        else:
            print("Operación cancelada")
    else:
        print("Producto no encontrado")

def menu_ventas(conn):
    while True:
        print("\n--- GESTIÓN DE VENTAS ---")
        print("1. Registrar nueva venta")
        print("2. Consultar ventas por fecha")
        print("3. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            registrar_venta_interactivo(conn)
        elif opcion == "2":
            consultar_ventas_fecha_interactivo(conn)
        elif opcion == "3":
            break
        else:
            print("Opción no válida")

def registrar_venta_interactivo(conn):
    print("\n--- REGISTRAR VENTA ---")
    productos_vendidos = []
    total = 0
    
    while True:
        codigo = input("Código del producto (dejar vacío para terminar): ")
        if not codigo:
            break
            
        detalle = obtener_detalle_venta(conn, codigo)
        if not detalle:
            print("Producto no encontrado")
            continue
            
        nombre, precio_venta = detalle
        print(f"Producto: {nombre} - Precio: {precio_venta:.2f}")
        
        try:
            cantidad = int(input("Cantidad: "))
            descuento = float(input("Descuento (%): ") or 0)
            vendedor = input("Vendedor: ") or "Sistema"
            
            # Crear venta
            venta = Venta(codigo, cantidad, descuento, vendedor)
            if registrar_venta(conn, venta):
                subtotal = precio_venta * cantidad * (1 - descuento/100)
                productos_vendidos.append({
                    'nombre': nombre,
                    'cantidad': cantidad,
                    'precio': precio_venta,
                    'descuento': descuento,
                    'subtotal': subtotal,
                    'vendedor': vendedor
                })
                total += subtotal
        except ValueError as e:
            print(f"Error: {e}")
    
    # Mostrar ticket
    if productos_vendidos:
        # Código para calcular el cambio
        while True:
            try:
                efectivo_recibido = float(input("Efectivo recibido: "))
                if efectivo_recibido < total:
                    print(f"Error: El efectivo ({efectivo_recibido:.2f}) no cubre el total ({total:.2f}). Intente nuevamente.")
                else:
                    cambio = efectivo_recibido - total
                    break  # Salir del bucle si el pago es suficiente
            except ValueError:
                print("Error: Ingrese un valor numérico válido")

        print("\n--- TICKET DE VENTA ---")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"Hora: {datetime.now().strftime('%H:%M:%S')}")
        print("{:<20} {:<10} {:<10} {:<10} {:<10} {:<10}".format(
            "Producto", "Cantidad", "P. Unit.", "Desc.%", "Subtotal", "Vendedor"
        ))
        print("-" * 80)
        for prod in productos_vendidos:
            print("{:<20} {:<10} {:<10.2f} {:<10.2f} {:<10.2f} {:<10}".format(
                prod['nombre'],
                prod['cantidad'],
                prod['precio'],
                prod['descuento'],
                prod['subtotal'],
                prod['vendedor']
            ))
        print("-" * 80)
        print(f"TOTAL A PAGAR: {total:.2f}")
        print(f"Efectivo recibido: {efectivo_recibido:.2f}")
        print(f"Cambio a devolver: {cambio:.2f}\n")

def consultar_ventas_fecha_interactivo(conn):
    print("\n--- CONSULTAR VENTAS POR FECHA ---")
    fecha_inicio = input("Fecha inicial (YYYY-MM-DD): ")
    fecha_fin = input("Fecha final (YYYY-MM-DD): ")
    
    ventas = consultar_ventas_por_fecha(conn, fecha_inicio, fecha_fin)
    if not ventas:
        print("No hay ventas en el rango especificado")
        return
    
    print("\n{:<10} {:<8} {:<20} {:<8} {:<10} {:<8} {:<10} {:<10}".format(
        "Fecha", "Hora", "Producto", "Cant.", "P. Unit.", "Desc.%", "Subtotal", "Vendedor"
    ))
    print("-" * 90)
    
    for venta in ventas:
        subtotal = venta[3] * venta[4] * (1 - venta[5]/100)
        print("{:<10} {:<8} {:<20} {:<8} {:<10.2f} {:<8.2f} {:<10.2f} {:<10}".format(
            venta[0], venta[1], venta[2], venta[3], venta[4], venta[5], subtotal, venta[6]
        ))

def menu_reportes(conn):
    while True:
        print("\n--- REPORTES ---")
        print("1. Exportar ventas a CSV")
        print("2. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            exportar_csv_interactivo(conn)
        elif opcion == "2":
            break
        else:
            print("Opción no válida")

def exportar_csv_interactivo(conn):
    print("\n--- EXPORTAR VENTAS A CSV ---")
    fecha_inicio = input("Fecha inicial (YYYY-MM-DD): ")
    fecha_fin = input("Fecha final (YYYY-MM-DD): ")
    archivo = input("Nombre del archivo CSV (ej: ventas_2023.csv): ")
    
    if exportar_reporte_csv(conn, fecha_inicio, fecha_fin, archivo):
        print(f"Reporte exportado exitosamente a {archivo}")
    else:
        print("Error al exportar el reporte")

def main():
    conn = crear_conexion()
    if conn is not None:
        verificar_tablas(conn)
    else:
        print("Error! No se puede conectar a la base de datos")
        return
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            menu_productos(conn)
        elif opcion == "2":
            menu_ventas(conn)
        elif opcion == "3":
            menu_reportes(conn)
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
    
    if conn:
        conn.close()

if __name__ == "__main__":
    main()
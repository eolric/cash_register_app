class Producto:
    def __init__(self, codigo, nombre, cantidad, precio_compra, precio_venta):
        self.codigo = codigo
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
    
    def to_dict(self):
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'precio_compra': self.precio_compra,
            'precio_venta': self.precio_venta
        }
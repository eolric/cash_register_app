from datetime import datetime

class Venta:
    def __init__(self, codigo_producto, cantidad, descuento=0, vendedor="Sistema"):
        self.codigo_producto = codigo_producto
        self.cantidad = cantidad
        self.descuento = descuento
        self.vendedor = vendedor
        self.fecha = datetime.now().strftime("%Y-%m-%d")
        self.hora = datetime.now().strftime("%H:%M:%S")
    
    def to_dict(self):
        return {
            'fecha': self.fecha,
            'hora': self.hora,
            'codigo_producto': self.codigo_producto,
            'cantidad': self.cantidad,
            'descuento': self.descuento,
            'vendedor': self.vendedor
        }
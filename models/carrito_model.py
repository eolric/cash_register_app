class CarritoCompras:
    def __init__(self):
        self.items = []
        
    def agregar_item(self, codigo, nombre, cantidad, precio, descuento=0, vendedor=""):
        subtotal = cantidad * precio * (1 - descuento/100)
        self.items.append({
            'codigo': codigo,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'descuento': descuento,
            'subtotal': subtotal,
            'vendedor': vendedor
        })
        return subtotal
        
    def calcular_total(self):
        return sum(item['subtotal'] for item in self.items)
        
    def vaciar(self):
        self.items = []
        
    def obtener_items(self):
        return self.items.copy()
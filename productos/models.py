from django.db import models
from tipos_productos.models import TipoProducto

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo_barras = models.CharField(max_length=13, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_caducidad = models.DateTimeField()
    cantidad_inventario = models.PositiveIntegerField()
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)

    def _str_(self):
        return self.nombre
    
class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    finalizada = models.BooleanField(default=False)

    def calcular_total(self):
        transacciones = Transaccion.objects.filter(id_venta=self)
        total = sum(transaccion.calcular_subtotal() for transaccion in transacciones)
        return total

    def _str_(self):
        return f'Venta {self.id_venta}'



class Transaccion(models.Model):
    id_transaccion = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    finalizada = models.BooleanField(default=False)
    
    def calcular_subtotal(self):
        return self.cantidad * self.id_producto.precio

    def _str_(self):
        return f'Transacción: {self.id_producto.nombre} en Venta {self.id_venta.id}'
from django.db import models
from tipos_productos.models import TipoProducto
# from datetime import timezone

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo_barras = models.CharField(max_length=13, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_caducidad = models.DateTimeField()
    #precio_costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    #precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    #precio_mayoreo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    #fecha_registro = models.DateTimeField(default=timezone.now)
    cantidad_inventario = models.PositiveIntegerField()
    #inventario_minimo = models.PositiveIntegerField(default=0)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    

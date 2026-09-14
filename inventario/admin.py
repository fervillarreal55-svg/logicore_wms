from django.contrib import admin
from .models import (
    Almacen, Zona, Ubicacion, Categoria, Unidad, Proveedor, 
    Producto, Cliente, Existencia, MovimientoInventario, 
    OrdenRecepcion, LineaRecepcion, PedidoDespacho, LineaDespacho
)

admin.site.register(Almacen)
admin.site.register(Zona)
admin.site.register(Ubicacion)
admin.site.register(Categoria)
admin.site.register(Unidad)
admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Existencia)
admin.site.register(MovimientoInventario)
admin.site.register(OrdenRecepcion)
admin.site.register(LineaRecepcion)
admin.site.register(PedidoDespacho)
admin.site.register(LineaDespacho)
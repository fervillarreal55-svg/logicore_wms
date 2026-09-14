from django.db import models

class Almacen(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Zona(models.Model):
    nombre = models.CharField(max_length=100)
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.almacen.nombre})"

class Ubicacion(models.Model):
    codigo = models.CharField(max_length=50, unique=True) # Formato pasillo-rack-nivel ej: A-01-01
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    capacidad = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.codigo

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Unidad(models.Model):
    nombre = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=10)

    def __str__(self):
        return self.abreviatura

class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sku} - {self.nombre}"

class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    ruc = models.CharField(max_length=20, unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Existencia(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    lote = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('producto', 'ubicacion', 'lote')

    def __str__(self):
        return f"{self.producto.nombre} | Lote: {self.lote} | Cant: {self.cantidad}"

class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('TRASLADO', 'Traslado'),
        ('INTENTO_FALLIDO', 'Intento Fallido'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    detalles = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"

class OrdenRecepcion(models.Model):
    ESTADOS = [('PENDIENTE', 'Pendiente'), ('COMPLETADA', 'Completada')]
    numero = models.CharField(max_length=50, unique=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

    def __str__(self):
        return f"OC: {self.numero}"

class LineaRecepcion(models.Model):
    orden = models.ForeignKey(OrdenRecepcion, related_name='lineas', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_esperada = models.PositiveIntegerField()
    cantidad_recibida = models.PositiveIntegerField(default=0)

class PedidoDespacho(models.Model):
    ESTADOS = [('PENDIENTE', 'Pendiente'), ('APROBADO', 'Aprobado'), ('COMPLETADO', 'Completado')]
    PRIORIDADES = [('BAJA', 'Baja'), ('NORMAL', 'Normal'), ('ALTA', 'Alta')]
    numero = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='NORMAL')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

    def __str__(self):
        return f"Pedido: {self.numero} ({self.prioridad})"

class LineaDespacho(models.Model):
    pedido = models.ForeignKey(PedidoDespacho, related_name='lineas', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
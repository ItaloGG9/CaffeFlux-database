from django.db import models

class JerarquiaProducto(models.Model):
    nombre_jerarquia = models.CharField(max_length=100)
    id_categoria = models.IntegerField(null=True, blank=True)
    id_subcategoria = models.IntegerField(null=True, blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_jerarquia

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    jerarquia = models.ForeignKey(JerarquiaProducto, related_name="productos", on_delete=models.SET_NULL, null=True, blank=True)
    estado_producto = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_producto

class Turno(models.Model):
    usuario_responsable = models.CharField(max_length=100)
    hora_apertura = models.DateTimeField()
    fondo_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    hora_cierre = models.DateTimeField(null=True, blank=True)
    usuario_cierre = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Turno {self.id} - {self.usuario_responsable}"

class Mesa(models.Model):
    estado_mesa = models.CharField(max_length=50)
    hora_apertura = models.DateTimeField(null=True, blank=True)
    hora_cierre = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Mesa {self.id} - {self.estado_mesa}"

class Pedido(models.Model):
    mesa = models.ForeignKey(Mesa, related_name="pedidos", on_delete=models.SET_NULL, null=True, blank=True)
    turno = models.ForeignKey(Turno, related_name="pedidos", on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=50, blank=True)
    precio_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.mesa_id}"

class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="lineas", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre_producto}"

class Pago(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="pagos", on_delete=models.CASCADE)
    metodo = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.id} - {self.monto}"

from django.contrib import admin
from .models import Producto, JerarquiaProducto, Turno, Mesa, Pedido, LineaPedido, Pago

admin.site.register(Producto)
admin.site.register(JerarquiaProducto)
admin.site.register(Turno)
admin.site.register(Mesa)
admin.site.register(Pedido)
admin.site.register(LineaPedido)
admin.site.register(Pago)

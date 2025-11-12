from rest_framework import viewsets
from .models import Producto, JerarquiaProducto, Turno, Mesa, Pedido, LineaPedido, Pago
from .serializers import (
    ProductoSerializer, JerarquiaProductoSerializer, TurnoSerializer,
    MesaSerializer, PedidoSerializer, LineaPedidoSerializer, PagoSerializer
)

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class JerarquiaProductoViewSet(viewsets.ModelViewSet):
    queryset = JerarquiaProducto.objects.all()
    serializer_class = JerarquiaProductoSerializer

class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer

class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class LineaPedidoViewSet(viewsets.ModelViewSet):
    queryset = LineaPedido.objects.all()
    serializer_class = LineaPedidoSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

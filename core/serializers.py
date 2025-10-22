from rest_framework import serializers
from .models import Producto, JerarquiaProducto, Turno, Mesa, Pedido, LineaPedido, Pago

class JerarquiaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = JerarquiaProducto
        fields = "__all__"

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = "__all__"

class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = "__all__"

class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = "__all__"

class LineaPedidoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    producto_id = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all(), source='producto', write_only=True)
    class Meta:
        model = LineaPedido
        fields = ["id", "pedido", "producto", "producto_id", "cantidad", "precio_unitario"]

class PedidoSerializer(serializers.ModelSerializer):
    lineas = LineaPedidoSerializer(many=True, read_only=True)
    class Meta:
        model = Pedido
        fields = "__all__"

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = "__all__"

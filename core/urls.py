from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    ProductoViewSet, JerarquiaProductoViewSet, TurnoViewSet,
    MesaViewSet, PedidoViewSet, LineaPedidoViewSet, PagoViewSet
)

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'jerarquias', JerarquiaProductoViewSet)
router.register(r'turnos', TurnoViewSet)
router.register(r'mesas', MesaViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'lineas', LineaPedidoViewSet)
router.register(r'pagos', PagoViewSet)

urlpatterns = [path("", include(router.urls))]

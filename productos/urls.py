from django.urls import path
from .views import listar_productos, registrar_producto, index, modificar_producto, base, eliminar_producto, buscar_productos
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.login_view, name='login'),  # Página de inicio de sesión como página principal
    path('base/', base, name='hogar'),
    path('inicio/', index, name='home'),  # Página anterior como página principal después de iniciar sesión
    path('listar/', listar_productos, name='listar_productos'),
    path('registrar/', views.registrar_producto, name='registrar_producto'),
    path('modificar/<int:id>/', login_required(modificar_producto), name='modificar_producto'),
    path('eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('registro/', views.registro_view, name='registro'),
    path('buscar/', buscar_productos, name='buscar_productos'),
    path('alertas/', views.alertas_bajo_inventario, name='alertas_productos'),
    path('detalle/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('crear/', views.crear_venta, name='crear_venta'),
    path('agregar_transaccion/<int:venta_id>/', views.agregar_transaccion, name='agregar_transaccion'),
    path('mostrar_ventas/', views.mostrar_ventas, name='mostrar_ventas'),
    
]




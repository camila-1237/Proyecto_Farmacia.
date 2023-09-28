from django.urls import path
from .views import listar_productos, registrar_producto, index, modificar_producto, base, eliminar_producto, buscar_productos
from . import views

urlpatterns = [
    path('base/', base, name='hogar'),
    path('', index, name='home'),
    path('listar/', listar_productos, name='listar_productos'),
    path('registrar/', views.registrar_producto, name='registrar_producto'),
    path('modificar/<id>/', modificar_producto, name='modificar_producto'),
    path('eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('buscar/',buscar_productos, name='buscar_productos'),

]


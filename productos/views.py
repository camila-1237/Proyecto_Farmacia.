from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import ProductoForm
from .models import Producto
from .models import TipoProducto
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# from .models import Venta, Transaccion
# from .forms import VentaForm, TransaccionForm


def cerrar_sesion(request):
    logout(request)
    return redirect('login')

def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirigir al usuario a la página de inicio
            return redirect('home')  # Asegúrate de que 'home' sea el nombre correcto de tu URL de inicio
        else:
            # Manejar el caso en que las credenciales de inicio de sesión no sean válidas
            # Puedes mostrar un mensaje de error o realizar otras acciones
            pass

    return render(request, 'registration/login.html')


def registro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está registrado.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)
                    return redirect('login')  # Redirige al inicio de sesión después del registro
        else:
            messages.error(request, 'Las contraseñas no coinciden.')

    return render(request, 'registration/registro.html')

def index( request ):
    return render(request, 'index.html')

def base( request ):
    return render(request, 'base.html')

@login_required
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/listar_productos.html', {'productos': productos})

@login_required
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

from datetime import datetime
@login_required
def registrar_producto(request):
    tipos = TipoProducto.objects.all()

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()

    hoy = datetime.today().strftime('%Y-%m-%d')

    return render(request, 'productos/registrar_producto.html', {'form': form, 'tipos': tipos, 'hoy': hoy})
def modificar_producto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    tipos = TipoProducto.objects.all()
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
        
    return render(request, 'productos/modificar_producto.html', {'form': form, 'tipos': tipos})


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')

    return render(request, 'productos/eliminar_productos.html', {'producto': producto})

#JuanJo

def buscar_productos(request):
    if request.method == 'GET':
        consulta = request.GET.get('consulta')
        resultados = Producto.objects.filter(
            Q(nombre__icontains=consulta) |  
            Q(codigo_barras__icontains=consulta)  
            
        )

    return render(request, 'productos/buscador.html', {'resultados': resultados})


def alertas_bajo_inventario(request):
    if request.method == 'GET':
        # Consulta para obtener los productos con inventario bajo
        productos_inventario_bajo = Producto.objects.filter(
            cantidad_inventario__lte=10
        )

        # Consulta para obtener los productos próximos a vencer (por ejemplo, en los próximos 30 días)
        fecha_actual = timezone.now()
        fecha_limite = fecha_actual + timezone.timedelta(days=3)
        productos_proximos_a_vencer = Producto.objects.filter(
            Q(fecha_caducidad__gte=fecha_actual) & Q(fecha_caducidad__lte=fecha_limite)
        )

    return render(request, 'productos/alertas.html', {
        'productos_inventario_bajo': productos_inventario_bajo,
        'productos_proximos_a_vencer': productos_proximos_a_vencer,
    })

# def crear_venta(request):
#     if request.method == 'POST':
#         venta_form = VentaForm(request.POST)
#         if venta_form.is_valid():
#             venta = venta_form.save(commit=False)
#             if venta.finalizada:
#                 venta.save()
#                 nueva_venta = Venta.objects.create()
#                 return redirect('agregar_transaccion', venta_id=nueva_venta.id_venta)
#             else:
#                 venta.save()
#                 return redirect('agregar_transaccion', venta_id=venta.id_venta)
#     else:
#         venta_form = VentaForm()
    
#     context = {
#         'venta_form': venta_form,
#     }
#     return render(request, 'venta/crear_venta.html', context)

# from .forms import TransaccionForm
# from .models import Venta, Producto


# from django.contrib import messages
# from django.contrib import messages

# def agregar_transaccion(request, venta_id):
#     venta = Venta.objects.get(id_venta=venta_id)
    
#     if request.method == 'POST':
#         transaccion_form = TransaccionForm(request.POST)
#         if transaccion_form.is_valid():
#             transaccion = transaccion_form.save(commit=False)
#             transaccion.id_venta = venta
#             if transaccion_form.cleaned_data['finalizada']:
#                 transaccion.finalizada = True

#             producto = transaccion.id_producto
#             cantidad_transaccion = transaccion.cantidad

#             producto.cantidad_inventario -= cantidad_transaccion
#             producto.save()

#             transaccion.save()
            
#             if transaccion.finalizada:
#                 nueva_venta = Venta.objects.create()
#                 return redirect('agregar_transaccion', venta_id=nueva_venta.id_venta)
#     else:
#         transaccion_form = TransaccionForm()  
    
#     context = {
#         'venta': venta,
#         'transaccion_form': transaccion_form,
#     }
#     return render(request, 'venta/agregar_transaccion.html', context)

# def mostrar_ventas(request):
#     ventas = Venta.objects.all()
    
#     context = {
#         'ventas': ventas,
#     }
#     return render(request, 'venta/mostrar_ventas.html', context)


# def crear_venta(request):
#     if request.method == 'POST':
#         venta_form = VentaForm(request.POST)
#         if venta_form.is_valid():
#             venta = venta_form.save(commit=False)
#             if venta.finalizada:
#                 venta.save()
#                 nueva_venta = Venta.objects.create()
#                 return redirect('agregar_transaccion', venta_id=nueva_venta.id_venta)
#             else:
#                 venta.save()
#                 return redirect('agregar_transaccion', venta_id=venta.id_venta)
#     else:
#         venta_form = VentaForm()
    
#     context = {
#         'venta_form': venta_form,
#     }
#     return render(request, 'venta/crear_venta.html', context)


# # def agregar_transaccion(request, venta_id):
# #     venta = Venta.objects.get(id_venta=venta_id)
    
# #     if request.method == 'POST':
# #         transaccion_form = TransaccionForm(request.POST)
# #         if transaccion_form.is_valid():
# #             transaccion = transaccion_form.save(commit=False)
# #             transaccion.id_venta = venta
# #             if transaccion_form.cleaned_data['finalizada']:
# #                 transaccion.finalizada = True

# #             producto = transaccion.id_producto
# #             cantidad_transaccion = transaccion.cantidad

# #             producto.cantidad_inventario -= cantidad_transaccion
# #             producto.save()

# #             transaccion.save()
            
# #             if transaccion.finalizada:
# #                 nueva_venta = Venta.objects.create()
# #                 return redirect('agregar_transaccion', venta_id=nueva_venta.id_venta)
# #     else:
# #         transaccion_form = TransaccionForm()  
    
# #     context = {
# #         'venta': venta,
# #         'transaccion_form': transaccion_form,
# #     }
# #     return render(request, 'venta/agregar_transaccion.html', context)

# def mostrar_ventas(request):
#     ventas = Venta.objects.all()
    
#     context = {
#         'ventas': ventas,
#     }
#     return render(request, 'venta/mostrar_ventas.html', context)

from django.shortcuts import render
from .models import Producto

def venta(request):
    productos = Producto.objects.all()
    return render(request, 'venta/venta.html', {'productos': productos})
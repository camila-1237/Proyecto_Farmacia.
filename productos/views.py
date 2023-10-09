from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import ProductoForm
from .models import Producto
from .models import TipoProducto
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib import messages

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
            user = User.objects.create_user(username=username, email=email, password=password1)
            return redirect('login')  

    return render(request, 'registration/registro.html')

def index( request ):
    return render(request, 'index.html')

def base( request ):
    return render(request, 'base.html')

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/listar_productos.html', {'productos': productos})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

def registrar_producto(request):
    tipos = TipoProducto.objects.all()  # Mueve esta línea aquí para asegurarte de que 'tipos' esté definida

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            productos = Producto.objects.all()
            # Redirigir al usuario a la página de listado de productos
            return redirect('listar_productos')
    else: 
        form = ProductoForm()
        hoy = datetime.today().strftime('%Y-%m-%d')

    return render(request, 'productos/registrar_producto.html', {'form': form, 'tipos': tipos})

def modificar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
        tipos = TipoProducto.objects.all()
    return render(request, 'productos/modificar_producto.html', {'form': form, 'tipos': tipos})


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')

    return render(request, 'productos/eliminar_productos.html', {'producto': producto})


#JuanJo

def buscar_productos(request):
    if request.method == 'GET':
        consulta = request.GET.get('consulta')
        resultados = Producto.objects.filter(
            Q(id__icontains=consulta) |
            Q(nombre__icontains=consulta) |
            Q(codigo_barras__icontains=consulta) |
            Q(precio__icontains=consulta) |
            Q(cantidad_inventario__icontains=consulta) |
            Q(tipo__nombre__icontains=consulta)
        )

    return render(request, 'productos/buscador.html', {'resultados':resultados})


def alertas_bajo_inventario(request):
    if request.method == 'GET':
        parametros = request.GET
        parametros = Producto.objects.filter(
            Q(cantidad_inventario__lte=10)     
        )   

        if parametros.exists():
            messages.success(request, "Productos con inventario bajo")
            
        #else: messages.success(request, "No hay productos con bajo inventario")

    return render(request, 'productos/alertas.html', {'parametros': parametros})
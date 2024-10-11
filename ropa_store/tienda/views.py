from django.shortcuts import render, redirect
from .models import Producto, Carrito
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

def index(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/index.html', {'productos': productos})

@login_required
def carrito_view(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    return render(request, 'tienda/carrito.html', {'carrito': carrito})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'tienda/login.html')

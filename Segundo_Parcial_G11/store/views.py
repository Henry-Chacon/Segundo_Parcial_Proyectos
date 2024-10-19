from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import json 
from django.http import Http404
from django.db import connection
from .forms import CustomUserCreationForm
from django.shortcuts import redirect, get_object_or_404
from .models import Cart, CartItem
from django.shortcuts import render
from .models import Product
from django.conf import settings
from django.core.mail import send_mail



def Tienda(request):
    return render(request,'store.html')

def cart(request):
    context = {}
    return render(request,'cart.html')

def checkout(request):
    context = {}
    return render(request,'checkout.html')

def direccion(request):
    context = {}
    return render(request,'direccion.html')

def tommy1(request):
    context = {}
    return render(request,'tommy1.html')
def tommy2(request):
    return render(request,'tommy2.html')
def tommy3(request):
    return render(request,'tommy3.html')

def boss1(request):
    context = {}
    return render(request,'boss1.html')
def boss2(request):
    return render(request,'boss2.html')
def boss3(request):
    return render(request,'boss3.html')

def lauren1(request):
    context = {}
    return render(request,'lauren1.html')
def lauren2(request):
    return render(request,'lauren2.html')
def lauren3(request):
    return render(request,'lauren3.html')

def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def enviar_correo(request, user_id):
    User = get_user_model()  # Obtén el modelo de usuario personalizado
    usuario = get_object_or_404(User, id=user_id)  # Obtén el usuario por su ID

    email_destinatario = usuario.email
    asunto = 'Bienvenido a nuestra tienda'
    mensaje = 'Gracias por registrarte. ¡Esperamos que disfrutes tu experiencia!'

    try:
        send_mail(  # Asegúrate de tener correctamente configurado el envío de correos
            asunto,
            mensaje,
            settings.EMAIL_HOST_USER,
            [email_destinatario],
            fail_silently=False,
        )
        messages.success(request, 'Correo de bienvenida enviado exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al enviar el correo: {e}')

    return redirect('thank')  # Redirige a la página 'thank.html'


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu cuenta ha sido creada exitosamente.')
            return redirect('login')
        else:
            messages.error(request, 'Error al registrar el usuario. Verifica los datos e intenta de nuevo.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_item_price = product.price * quantity
        total_price += total_item_price

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'get_total_price': total_item_price
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'cart.html', context)

def clear_cart(request):
    request.session['cart'] = {}
    return redirect('cart_view')

def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def store_view(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store.html', context)
#---------------------------------------------------------------------------------------------------
def update_cart_sum(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})

        if cart[str(product_id)] < 10:  # Limitar a un máximo de 10
            cart[str(product_id)] += 1
            request.session['cart'] = cart
            messages.success(request, f'El producto {product.name} ha sido agregado al carrito.')
        else:
            messages.info(request, f'Límite de productos alcanzados')
    except Product.DoesNotExist:
        messages.error(request, 'Error: el producto no existe.')
    except Exception as e:
        messages.error(request, 'Ha ocurrido un error al agregar el producto al carrito.')

    request.session['cart'] = cart

    return redirect('cart_view')

#---------------------------------------------
def update_cart_res(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})

        if cart[str(product_id)] > 0:  # Limitar a un máximo de 10
            cart[str(product_id)] -= 1
            request.session['cart'] = cart
            messages.success(request, f'El producto {product.name} ha sido removido del carrito.')
        elif cart[str(product_id)] == 0:
            cart = [item for item in cart if item['product_id'] != product_id]
    except Product.DoesNotExist:
        messages.error(request, 'Error: el producto no existe.')
    except Exception as e:
        messages.error(request, 'Ha ocurrido un error al agregar el producto al carrito.')

    request.session['cart'] = cart

    return redirect('cart_view')

#---------------------------------------------
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)] += 1 
        else:
            cart[str(product_id)] = 1

        # Guardar el carrito en la sesión
        request.session['cart'] = cart
        messages.success(request, f'El producto {product.name} ha sido agregado al carrito.')
    except Product.DoesNotExist:
        messages.error(request, 'Error: el producto no existe.')
    except Exception as e:
        messages.error(request, 'Ha ocurrido un error al agregar el producto al carrito.')

    return redirect('Tienda')
#---------------------------------------------
def remove_from_cart(request, product_id):
    # Obtener el producto que se quiere eliminar
    product = get_object_or_404(Product, id=product_id)

    # Obtener el carrito de la sesión
    cart = request.session.get('cart', [])

    # Filtrar el carrito para eliminar solo el producto específico
    cart = [item for item in cart if item['product_id'] != product_id]

    # Guardar el carrito actualizado en la sesión
    request.session['cart'] = cart

    # Mensaje de éxito
    messages.success(request, f'El producto {product.name} ha sido removido del carrito.')

    return redirect('cart_view')




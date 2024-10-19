from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.apps import apps
from django.utils.deprecation import MiddlewareMixin

class CustomUser(AbstractUser):
    usname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=8)
    email = models.CharField(max_length=255)



    def __str__(self):
        return self.username
    


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)  # Uso de 'app_label.ModelName'
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity


class CartMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Inicializar el carrito en la sesión si no existe
        if 'cart' not in request.session:
            request.session['cart'] = []

    def add_to_cart(self, request, product_id, quantity):
        # Obtener el carrito de la sesión
        cart = request.session.get('cart', [])

        # Verificar si el producto ya está en el carrito
        product_exists = False
        for item in cart:
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                product_exists = True
                break

        # Si el producto no está en el carrito, agregarlo
        if not product_exists:
            cart.append({'product_id': product_id, 'quantity': quantity})

        # Guardar el carrito de nuevo en la sesión
        request.session['cart'] = cart


    def process_view(self, request, view_func, view_args, view_kwargs):
        # Maneja la lógica de agregar productos al carrito desde cualquier vista
        if request.method == 'POST' and 'add_to_cart' in request.POST:
            product_id = int(request.POST.get('product_id'))
            quantity = int(request.POST.get('quantity'))
            self.add_to_cart(request, product_id, quantity)

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.CharField(max_length=255, blank=True)
    stock = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
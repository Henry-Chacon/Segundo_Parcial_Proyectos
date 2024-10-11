from django.urls import path
from .views import index, carrito_view, login_view

urlpatterns = [
    path('', index, name='index'),
    path('carrito/', carrito_view, name='carrito'),
    path('login/', login_view, name='login'),
]

from django.urls import path
from .views import (
    store,
    cart,
    cart_response,
    checkout,
    updateCartItem,
    cart_item,
    productsImage,
)

app_name = 'store'

urlpatterns = [
    path('', store, name='store'),
    path('cart/', cart, name='cart'),
    path('cart_response/', cart_response, name='cart_response'),
    path('checkout/', checkout, name='checkout'),
    path('cartlist/', cart_item, name='cartlist'),
    path('update_cart/', updateCartItem, name='update_cart'),
    path('images/', productsImage, name='images'),
]

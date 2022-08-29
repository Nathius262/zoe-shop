from django.urls import path
from .views import (
    store,
    cart,
    checkout,
)

app_name = 'store'

urlpatterns = [
    path('', store, name='store'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
]

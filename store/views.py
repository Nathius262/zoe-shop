from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import json
from .models import *


# Create your views here.
def cart_item(request):
	context = {}
	if request.user.is_authenticated:
		customer = request.user.customer
		order = Order.objects.get(customer=customer, complete=False)
		
		data={
			"get_cart_items":order.get_cart_items
		}
	return JsonResponse(data, content_type='application/json', safe=False)

def store(request):
	products = Product.objects.all()
	context = {
		'products':products
	}
	return render(request, "store/store.html", context)


def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer)
		item = order.orderitem_set.all()
	else:
		item = []
		order = {'get_cart_total':0, 'get_cart_items':0}

	context = {
		'item':item,
		'order':order
	}
	return render(request, "store/cart.html", context)

# cart api call
def data_obj(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		item = order.orderitem_set.all()
	else:
		item = []
		order = {'get_cart_total':0, 'get_cart_items':0}
	
	a= {}
	data=[]
	for items in item:
		a= { 
			'productId':items.product.id,
			'productName': items.product.name,
			'productPrice':items.product.price,
			'productImage':items.product.product_image_url,
			'quantity':items.quantity,
			'price':items.get_total,
		}
		data.append(a)
		a.update(a)
			

	item = item.first()
	b = {
		'quantityTotal': order.get_cart_items,
		'priceTotal': order.get_cart_total,
	}
	data.append(b)
	return data

def cart_response(request):	
	return JsonResponse(data_obj(request),  content_type='application/json', safe=False)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer)
		item = order.orderitem_set.all()
	else:
		item = []
		order = {'get_cart_total':0, 'get_cart_items':0}

	context = {
		'item':item,
		'order':order
	}
	return render(request, "store/checkout.html", context)


def updateCartItem(request):

	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
	item_quantity = orderItem.quantity
	if action == 'add':
		orderItem.quantity = (item_quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (item_quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse('Success', safe=False)


def productsImage(request):
	# products = Product.objects.all().filter(id=2)

	images = ProductImage.objects.get(pk=1)
	print(images)

	context = {
		'images':images
	}
	return render(request, "store/productsImage.html", context)
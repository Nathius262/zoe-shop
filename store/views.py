from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import json
from .models import *
from .utils import data_obj
import datetime


# Create your views here.
def cart_item(request):
	context = {}
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	
		data={
					"get_cart_items":order.get_cart_items
				}
	else:
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}

		cart_item = 0
		for i in cart:
			cart_item = cart_item + cart[i]["quantity"]
		data={
				"get_cart_items":cart_item
			}
		
		
	return JsonResponse(data, content_type='application/json', safe=False)

def store(request):
	
	products = Product.objects.all()
	context = {
		'products':products
	}
	return render(request, "store/store.html", context)


def cart(request):	
	return render(request, "store/cart.html")



def cart_response(request):	
	return JsonResponse(data_obj(request),  content_type='application/json', safe=False)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		item = order.orderitem_set.all()
	else:
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}

		total = 0	
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
		item = []	
		for i in cart:
			try:
				product = Product.objects.get(id=i)
				total = (product.price * cart[i]["quantity"])

				order['get_cart_total'] += total
				order['get_cart_items'] += cart[i]["quantity"]

				items = {
					'product':{
						'id':product.id,
						'name':product.name,
						'price':product.price,
						'product_image_url':product.product_image_url,
					},
					'quantity': cart[i]["quantity"],
					'get_total': total,
				}

				item.append(items)

				if product.digital ==False:
					order['shipping'] = True
			except:
				pass

	context = {
		'item':item,
		'order':order
	}
	return render(request, "store/checkout.html", context)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = data['form']['total']
		order.transaction_id =transaction_id



		if str(total) == str(order.get_cart_total):
			"""the reason why the condition is a string is because they are returning the same value but different format. unable to figure how to do that for now! """
			order.complete = True

		order.save()

		if order.shipping == True:
			ShippingAddress.objects.create(
				customer=customer,
				order=order,
				address = str(data['shipping']['address']),
				city = str(data['shipping']['city']),
				state = str(data['shipping']['state']),
				zipcode = str(data['shipping']['zipcode'])
			)

	else:
		print('user not logged in')
	return JsonResponse('payment complete', safe=False)


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
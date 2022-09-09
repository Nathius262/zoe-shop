from .models import *
# cart api call


def data_obj(request):
	data=[]
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		item = order.orderitem_set.all()
		a= {}
		
		for item in item:
			try:
				a= { 
					'productId':item.product.id,
					'productName': item.product.name,
					'productPrice':item.product.price,
					'productImage':item.product.product_image_url,
					'quantity':item.quantity,
					'price':item.get_total,
				}			

				a.update(a)
				data.append(a)

				data.append(b)
			except:
				pass

			b = {
				'quantityTotal': order.get_cart_items,
				'priceTotal': order.get_cart_total,
			}
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
					 
					'productId':product.id,
					'productName': product.name,
					'productPrice':product.price,
					'productImage':product.product_image_url,
					'quantity':cart[i]["quantity"],
					'price':total,
				}

				item.append(items)

				if product.digital ==False:
					order['shipping'] = True
			except:
				pass
		b = {
			'quantityTotal': order['get_cart_items'],
			'priceTotal': order['get_cart_total'],
		}
		data = item
		data.append(b)

	return data
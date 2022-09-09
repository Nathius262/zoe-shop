from django.db import models
from django.contrib.auth.models import User
import os
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


def product_image_location(instance, filename):
    file_path = 'product/{product_id}/product.jpeg'.format(
        product_id=str(instance.id), filename=filename
    )
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(full_path):
        os.remove(full_path)
    return file_path


def more_img_product(instance, filename):
	file_path = 'product/{product_id}/{img_porduct}_product.jpeg'.format(
	    product_id=str(instance.product_attr.id), img_porduct=str(instance.id), filename=filename
	)
	full_path = os.path.join(settings.MEDIA_ROOT, file_path)
	if os.path.exists(full_path):
	    os.remove(full_path)
	return file_path


# Create your models here.
class Customer(models.Model):
	"""docstring for Customer"""
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=200, null=True)
	email = models.EmailField(max_length=200, null=True)

	def __str__(self):
		return str(self.user)


class Product(models.Model):
	"""docstring for Product"""
	name = models.CharField(max_length=200, null=True)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	digital = models.BooleanField(default=False, null=True, blank=True)
	product_image = models.ImageField(upload_to=product_image_location, null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def product_image_url(self):
		try:
			url = self.product_image.url
		except:
			url = ""

		return url


class ProductImage(models.Model):
	"""docstring for ProductImage"""
	product_attr = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
	img_porduct = models.ImageField(upload_to=more_img_product, null=True, blank=True)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.id}'

	@property
	def product_image_url(self):
		try:
			url = self.img_porduct.url
		except:
			url = ""

		return url
		
	

class Order(models.Model):
	"""docstring for Order"""
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, null=True, blank=True)
	transaction_id = models.CharField(max_length=200, null=True)
		
	def __str__(self):
		return f'order_{self.id} by {self.customer}'

	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			try:
				if i.product.digital == False:
					shipping = True
			except AttributeError:
				pass
		return shipping
	

	@property
	def get_cart_total(self):
		total=0
		try:
			orderitems = self.orderitem_set.all()
			# total = sum([item.get_total for item in orderitems])

			for item in orderitems:
				total += item.get_total
			
		except AttributeError :
			pass
		
		return total

	@property
	def get_cart_items(self):
		total=0
		try:
			orderitems = self.orderitem_set.all()
			# total = sum([item.quantity for item in orderitems])
			for item in orderitems:
				total += item.quantity
		except AttributeError :
			pass
		return total
	

class OrderItem(models.Model):
	"""docstring for OrderItem"""
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added  = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = 0
		try:
			total = self.product.price * self.quantity
		except AttributeError:
			pass
		return total

class ShippingAddress(models.Model):
	"""docstring for ShippingAddress"""
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	address = models.CharField(max_length=200, null=True)
	city = models.CharField(max_length=200, null=True)
	state = models.CharField(max_length=200, null=True)
	zipcode = models.CharField(max_length=200, null=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address


@receiver(post_save, sender=Product)
def save_product_img(sender, instance, *args, **kwargs):
    if instance.product_image:
        SIZE = 600, 600
        pic = Image.open(instance.product_image.path)
        if pic.mode in ("RGBA", 'P'):
            pic = pic.convert("RGB")
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(instance.product_image.path)
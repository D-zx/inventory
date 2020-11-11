from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.safestring import mark_safe
from datetime import datetime

# Create your models here.


class Item(models.Model):
	item_id = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	brand = models.CharField(max_length=100)
	item_type = models.CharField(max_length=100)
	description = models.CharField(max_length=200)
	pktsize = models.IntegerField(default=1)
	lifetime = models.CharField(max_length=100)
	rmd_amount = models.IntegerField(default=0)
	stock = models.IntegerField(default=0)
	total_receive = models.IntegerField(default=0)
	total_sale = models.IntegerField(default=0)
	

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('inventory:item_list')

	def need_remind(self):
		stock = self.stock
		rmd = self.rmd_amount
		if stock <= rmd:
			return mark_safe("<span class='new badge red' data-badge-caption='Restock'></span>")
		else:
			return mark_safe("")


	def update_stock(self):
		stock = 0
		total_sale = 0
		total_receive = 0
		for obj in self.inventoryupdate_set.all():
			if obj.process == 'receive':
				stock += obj.quantity
				total_receive += obj.quantity
			else:
				stock -= obj.quantity
				total_sale += obj.quantity
		self.stock = stock
		self.total_sale = total_sale
		self.total_receive = total_receive
		self.save()


class Inventory(models.Model):
	item = models.OneToOneField(Item, on_delete=models.CASCADE)
	stock = models.IntegerField(default=0)

	def __str__(self):
		return self.item.name

	def create_inventory(sender, **kwargs):
		if kwargs['created']:
			inventory = Inventory.objects.create(item=kwargs['instance'])
			inventory.save()

	post_save.connect(create_inventory, sender=Item)


class InventoryUpdate(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.IntegerField(null=False)
	process = models.CharField(max_length=100, blank=True)
	date = models.DateField(null=False, default=datetime.today)

	# def __str__(self):
	# 	return self.inventory+ '_' +self.uType +'_'+ str(self.date)

	def get_absolute_url(self):
		if self.process == 'receive':
			return reverse('inventory:receive_list')
		elif self.process == 'sale':
			return reverse('inventory:sale_list')

	# def update(self):
	# 	uType = self.uType
	# 	inventory = self.inventory
	# 	if uType == 'receive':
	# 		inventory.stock += self.quantity
	# 		inventory.save()
	# 		self.save()
	# 		return redirect('inventory:inventory')
	# 	elif uType == 'sale':
	# 		inventory.stock -= self.quantity
	# 		if inventory.stock < 0:
	# 			msg = "out of stock"
	# 			return redirect('inventory:inventoryupdate')
	# 		else:
	# 			inventory.save()
	# 			self.save()
	# 			return redirect('inventory:inventory')
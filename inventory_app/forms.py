from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import Item, Inventory, InventoryUpdate


class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ('item_id','name','brand','category','lifetime','pktsize','rmd_amount','description')
		exclude = ('stock',)
		labels = {
		'item_id': _('Item ID'),
		'name': _('Item Name'),
		'brand': _('Brand Name'),
		'category': _('Category'),
		'description': _('Description'),
		'lifetime': _('LifeTime'),
		'pktsize': _('Packet Size'),
		'rmd_amount': _('Reminder Limit'),
		}
		widgets = {
		'pktsize': forms.TextInput(attrs={'pattern':'\d*'}),
		'rmd_amount': forms.TextInput(attrs={'pattern':'\d*'}),
		}

class InventoryUpdateForm(forms.ModelForm):
	class Meta:
		model = InventoryUpdate
		fields= (
				'quantity',
				'date'
				)
		widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


	def clean(self):
		old = self.instance
		new = super().clean()
		qty = new.get('quantity') - old.quantity
		if old.id:
			total_sale = old.item.total_sale
			total_receive = old.item.total_receive
			process = old.process
			if process == 'receive':
				total_receive += qty
			else:
				total_sale += qty
			if total_receive < total_sale:
				self.add_error('quantity', "Invalid quantity to edit. Check inventory before edit")
		else:
			return new


from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Item, Inventory, InventoryUpdate


class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ('item_id','name','brand','item_type','description','lifetime','pktsize','rmd_amount')
		exclude = ('stock',)
		labels = {
		'item_id': _('Item ID'),
		'name': _('Item Name'),
		'brand': _('Brand Name'),
		'item_type': _('Category'),
		'description': _('Description'),
		'lifetime': _('LifeTime'),
		'pkgsize': _('Package Size'),
		'rmd_amount': _('Reminder Limit'),
		}
		# widgets = {
		# 'description': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
		# }

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

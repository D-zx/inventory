from django.shortcuts import render, redirect
from django.views.generic import (	TemplateView, ListView, DetailView,FormView,
                                    CreateView, UpdateView, DeleteView, RedirectView)

from .models import Item, Inventory, InventoryUpdate
from .forms import ItemForm, InventoryUpdateForm

from django.contrib import messages

# Create your views here.

class  Home(TemplateView):
	template_name = 'home/index.html'

	def get(self, request):
		return redirect('inventory:item_list')

class CreateItem(CreateView):
	model=Item
	form_class= ItemForm
	template_name='inventory/item_create.html'


class UpdateItem(UpdateView):
	model=Item
	form_class= ItemForm
	template_name='inventory/item_update.html'

class DeleteItem(DeleteView):
	model=Item

class ItemDetail(DetailView):
	model=Item
	template_name='inventory/item_detail.html'

class ItemList(ListView):
	model=Item
	template_name='inventory/inventory.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['brands'] = Item.objects.values_list('brand', flat=True).distinct()
		return context

	def get_queryset(self):
		search={}
		brand = self.request.GET.get('brand') or ''
		name = self.request.GET.get('item') or ''
		if brand:
			search['brand__iexact'] = brand
		search['name__contains'] = name
		queryset = super(ItemList, self).get_queryset()
		queryset = queryset.filter(**search).order_by('id')
		return queryset


class Receive(CreateView):
	model=InventoryUpdate
	form_class= InventoryUpdateForm
	template_name='receive_sale/receive.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['obj'] = Item.objects.get(pk=self.kwargs['pk'])
		return context

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		obj = Item.objects.get(pk=kwargs['pk'])
		if form.is_valid():
			form = form.save(commit=False)
			form.item = obj
			form.process = 'receive'
			obj.stock += form.quantity
			form.save()
			obj.save()
			return redirect('inventory:receive_list')

class ReceiveUpdate(UpdateView):
	model=InventoryUpdate
	form_class= InventoryUpdateForm
	template_name='receive_sale/receive.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		print(context)
		context['obj'] = InventoryUpdate.objects.get(pk=self.kwargs['pk']).item
		return context

	def form_valid(self, form):
		form.save()
		obj = InventoryUpdate.objects.get(pk=self.kwargs['pk']).item
		obj.update_stock()
		return super().form_valid(form)

		

class ReceiveList(ListView):
	model=InventoryUpdate
	template_name='receive_sale/receivelist.html'

	def get_queryset(self):
		search={}
		brand = self.request.GET.get('brand') or ''
		name = self.request.GET.get('item') or ''
		date = self.request.GET.get('date') or ''
		search['process__iexact'] = "receive"
		search['item__name__contains'] = name
		if brand:
			search['item__brand__iexact'] = brand
		if date:
			search['date'] = date
		queryset = super(ListView, self).get_queryset()
		queryset = queryset.filter(**search).order_by('id')
		return queryset



class Sale(CreateView):
	model=InventoryUpdate
	form_class= InventoryUpdateForm
	template_name='receive_sale/sale.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['obj'] = Item.objects.get(pk=self.kwargs['pk'])
		return context

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		obj = Item.objects.get(pk=kwargs['pk'])
		if form.is_valid():
			form1 = form.save(commit=False)
			form1.item = obj
			form1.process = 'sale'
			stock = obj.stock
			obj.stock -= form1.quantity
			if obj.stock < 0:
				self.object = form
				messages.add_message(self.request,messages.WARNING,"Out of Stock, only have %spkg instock " %stock)
				return self.render_to_response(self.get_context_data(form=form))
			else:
				form1.save()
				obj.save()
				return redirect('inventory:sale_list')
			

class SaleList(ListView):
	model=InventoryUpdate
	template_name='receive_sale/salelist.html'

	def get_queryset(self):
		search={}
		brand = self.request.GET.get('brand') or ''
		name = self.request.GET.get('item') or ''
		date = self.request.GET.get('date') or ''
		search['process__iexact'] = "sale"
		search['item__name__contains'] = name
		if brand:
			search['item__brand__iexact'] = brand
		if date:
			search['date'] = date
		queryset = super(ListView, self).get_queryset()
		queryset = queryset.filter(**search).order_by('id')
		return queryset
		

class SaleUpdate(UpdateView):
	model=InventoryUpdate
	form_class= InventoryUpdateForm
	template_name='receive_sale/sale.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		print(context)
		context['obj'] = InventoryUpdate.objects.get(pk=self.kwargs['pk']).item
		return context

	def form_valid(self, form):
		form.save()
		obj = InventoryUpdate.objects.get(pk=self.kwargs['pk']).item
		obj.update_stock()
		return super().form_valid(form)
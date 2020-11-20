from django.shortcuts import render, redirect
from django.views.generic import (	TemplateView, ListView, DetailView,FormView,
                                    CreateView, UpdateView, DeleteView, RedirectView)
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from .models import Item, Inventory, InventoryUpdate
from .forms import ItemForm, InventoryUpdateForm

from django.contrib import messages
from django.urls import path, reverse, reverse_lazy
from datetime import datetime


# Create your views here.

class  Home(LoginRequiredMixin,TemplateView):
	login_url = '/account/login'
	template_name = 'home/index.html'

	def get(self, request):
		return redirect('inventory:item_list')

class CreateItem(LoginRequiredMixin, CreateView):
	login_url = '/account/login'
	model=Item
	form_class= ItemForm
	template_name='inventory/item_create.html'


class UpdateItem(LoginRequiredMixin, UpdateView):
	login_url = '/account/login'
	model=Item
	form_class= ItemForm
	template_name='inventory/item_update.html'

class DeleteItem(LoginRequiredMixin, DeleteView):
	login_url = '/account/login'
	model=Item
	success_url = reverse_lazy('inventory_app:home')

	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

class ItemDetail(LoginRequiredMixin, DetailView):
	login_url = '/account/login'
	model=Item
	template_name='inventory/item_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		process = self.request.GET.get('process') or ''
		start = self.request.GET.get('start_date') or datetime.today()
		end = self.request.GET.get('end_date') or datetime.today()
		search= {}
		if process:
			search['process__iexact'] = process
		if start:
			search['date__range'] = [start, end]
		query = context['object'].inventoryupdate_set.all()
		query = query.filter(**search).order_by('id')
		context['process_list'] = query

		return context

class ItemList(LoginRequiredMixin, ListView):
	login_url = '/account/login'
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
		search['name__icontains'] = name
		queryset = super(ItemList, self).get_queryset()
		queryset = queryset.filter(**search).order_by('id')
		return queryset


class Receive(LoginRequiredMixin, CreateView):
	login_url = '/account/login'
	model=InventoryUpdate
	form_class= InventoryUpdateForm
	template_name='receive_sale/receive.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['obj'] = Item.objects.get(pk=self.kwargs['pk'])
		return context

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()
		obj = Item.objects.get(pk=kwargs['pk'])
		if form.is_valid():
			form = form.save(commit=False)
			form.item = obj
			form.process = 'receive'
			form.save()
			obj.update_stock()
			return redirect(reverse('inventory:item_detail', kwargs={'pk': obj.id}))
		else:
			return self.form_invalid(form)


class Sale(LoginRequiredMixin, CreateView):
	login_url = '/account/login'
	model=InventoryUpdate
	form_class= InventoryUpdateForm
	template_name='receive_sale/sale.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['obj'] = Item.objects.get(pk=self.kwargs['pk'])
		return context

	def post(self, request, *args, **kwargs):
		self.object = None
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
				obj.update_stock()
				return redirect(reverse('inventory:item_detail', kwargs={'pk': obj.id}))
		else:
			return self.form_invalid(form)
			

class ProcessList(LoginRequiredMixin, ListView):
	login_url = '/account/login'
	model=InventoryUpdate
	template_name='receive_sale/receive_list.html'
	process = 'receive'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['brands'] = Item.objects.values_list('brand', flat=True).distinct()
		return context

	def get_queryset(self):
		search={}
		brand = self.request.GET.get('brand') or ''
		name = self.request.GET.get('item') or ''
		start = self.request.GET.get('start_date') or datetime.today()
		end = self.request.GET.get('end_date') or datetime.today()
		search['process__iexact'] = self.process
		search['item__name__contains'] = name
		if brand:
			search['item__brand__iexact'] = brand
		if start:
			search['date__range'] = [start, end]
		queryset = super(ListView, self).get_queryset()
		queryset = queryset.filter(**search).order_by('id')
		return queryset
		

class ProcessUpdate(LoginRequiredMixin, UpdateView):
	login_url = '/account/login'
	model=InventoryUpdate
	form_class= InventoryUpdateForm
	template_name='receive_sale/sale.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['obj'] = InventoryUpdate.objects.get(pk=self.kwargs['pk']).item
		return context


	def form_valid(self, form):
		form.save()
		obj = InventoryUpdate.objects.get(pk=self.kwargs['pk']).item
		obj.update_stock()
		return super().form_valid(form)

class ProcessDelete(LoginRequiredMixin, DeleteView):
	login_url = '/account/login'
	model = InventoryUpdate
	success_url = reverse_lazy('inventory:receive_list')

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		item = self.object.item
		success_url = self.object.get_absolute_url()
		after = item.stock - self.object.quantity
		if after < 0:
			messages.add_message(self.request,messages.WARNING,"You cannot delete.")
			return redirect(success_url)
		else:
			self.object.delete()
			item.update_stock()
			return redirect(success_url)

from django.conf.urls import url
from django.urls import path, include
from .views import (CreateItem, UpdateItem, DeleteItem, ItemList, ItemDetail, 
                    Receive, Sale, ProcessList, ProcessUpdate, ProcessDelete,
                    Home)


app_name = 'inventory_app'


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('item/create', CreateItem.as_view(), name='item_create'),
    path('item/<pk>/update', UpdateItem.as_view(), name='item_udpate'),
    path('item/<pk>/delete', DeleteItem.as_view(), name='item_delete'),
    path('items/', ItemList.as_view(), name='item_list'),
    path('item/<pk>/', ItemDetail.as_view(), name='item_detail'),
    path('receive/<pk>/', Receive.as_view(), name='receive'),
    path('receivelist/', ProcessList.as_view(process='receive', template_name='receive_sale/receive_list.html'), name='receive_list'),
    path('receive_update/<pk>/', ProcessUpdate.as_view(template_name='receive_sale/receive.html'), name='receive_update'),
    path('sale/<pk>/', Sale.as_view(), name='sale'),
    path('salelist/', ProcessList.as_view(process='sale', template_name='receive_sale/sale_list.html'), name='sale_list'),
    path('sale_update/<pk>/', ProcessUpdate.as_view(template_name='receive_sale/sale.html'), name='sale_update'),
    path('process_delete/<pk>/', ProcessDelete.as_view(), name='process_delete'),

]


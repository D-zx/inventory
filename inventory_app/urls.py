from django.conf.urls import url
from django.urls import path, include
from .views import CreateItem, UpdateItem, DeleteItem, ItemList, ItemDetail, Receive, Sale, ReceiveList, SaleList, ReceiveUpdate, SaleUpdate


app_name = 'inventory_app'


urlpatterns = [
    path('item/create', CreateItem.as_view(), name='item_create'),
    path('item/<pk>/update', UpdateItem.as_view(), name='item_udpate'),
    path('item/<pk>/delete', DeleteItem.as_view(), name='item_delete'),
    path('items/', ItemList.as_view(), name='item_list'),
    path('item/<pk>/', ItemDetail.as_view(), name='item_detail'),
    path('receive/<pk>/', Receive.as_view(), name='receive'),
    path('receive_update/<pk>/', ReceiveUpdate.as_view(), name='receive_update'),
    path('receivelist/', ReceiveList.as_view(), name='receive_list'),
    path('sale/<pk>/', Sale.as_view(), name='sale'),
    path('salelist/', SaleList.as_view(), name='sale_list'),
    path('sale_update/<pk>/', SaleUpdate.as_view(), name='sale_update'),
]


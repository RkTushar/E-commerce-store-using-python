from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),  
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/invoice/', views.download_invoice, name='download_invoice'),
    path('my-orders/', views.my_orders, name='my_orders'),

    
]

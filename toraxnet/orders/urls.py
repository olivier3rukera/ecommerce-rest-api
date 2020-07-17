from django.urls import path
from .api import views

urlpatterns = [
    path('add-to-cart/', views.add_item_to_cart),
    path('user-cart/', views.CartUserListView.as_view()),
    path('update-cart/', views.update_cart),
    path('order-from-cart/', views.order_many_items),
    path('user-orders/', views.OrderListView.as_view()),
    path('order-single-item/', views.order_single_item),
    path('seller-orders/<uuid:uuid>/', views.OrderItemListView.as_view()),
    path('seller-orders/', views.OrderSellerListView.as_view())
]

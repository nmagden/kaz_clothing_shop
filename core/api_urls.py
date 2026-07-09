from django.urls import path
from . import api_views

urlpatterns = [
    path('categories/', api_views.category_list, name='api_category_list'),
    path('products/', api_views.product_list_api, name='api_product_list'),

    path('register/', api_views.register, name='api_register'),
    path('login/', api_views.login_view, name='api_login'),
    path('logout/', api_views.logout_view, name='api_logout'),

    path('orders/', api_views.OrderListCreateView.as_view(), name='api_order_list_create'),
    path('orders/<int:pk>/', api_views.OrderDetailView.as_view(), name='api_order_detail'),
]
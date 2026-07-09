from django.shortcuts import render
from .models import Product, Category


def home(request):
    categories = Category.objects.all()
    return render(request, 'core/home.html', {'categories': categories})


def product_list(request):
    products = Product.available.all()
    return render(request, 'core/product_list.html', {'products': products})
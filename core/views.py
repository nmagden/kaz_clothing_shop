from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Category, Order, OrderItem
from .forms import RegisterForm, LoginForm, ProductFilterForm, AddToOrderForm


def home(request):
    categories = Category.objects.all()
    return render(request, 'core/home.html', {'categories': categories})


def product_list(request):
    products = Product.available.all()
    form = ProductFilterForm(request.GET or None)

    if form.is_valid():
        category = form.cleaned_data.get('category')
        max_price = form.cleaned_data.get('max_price')
        if category:
            products = products.filter(category=category)
        if max_price:
            products = products.filter(price__lte=max_price)

    return render(request, 'core/product_list.html', {'products': products, 'form': form})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_available=True)
    add_form = AddToOrderForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Войдите в аккаунт, чтобы добавить товар в заказ')
            return redirect('login')

        add_form = AddToOrderForm(request.POST)
        if add_form.is_valid():
            order, _ = Order.objects.get_or_create(user=request.user, status='pending')
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=add_form.cleaned_data['quantity']
            )
            messages.success(request, f'{product.name} добавлен в заказ')
            return redirect('product_detail', pk=pk)
        else:
            messages.error(request, 'Проверьте количество')

    return render(request, 'core/product_detail.html', {'product': product, 'form': add_form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно')
            return redirect('home')
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Вы вошли в аккаунт')
            return redirect('home')
        else:
            messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта')
    return redirect('home')
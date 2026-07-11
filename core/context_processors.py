from .models import Order


def cart_info(request):
    if request.user.is_authenticated:
        pending_order = Order.objects.filter(user=request.user, status='pending').first()
        items_count = pending_order.items.count() if pending_order else 0
    else:
        items_count = 0
    return {'cart_items_count': items_count}
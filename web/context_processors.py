from product.models import Category, SubCategory
from django.db.models import Count
from web.cart import Cart
from accounts.models import User
from .models import Shipping


def main_context(request):
    header_category = Category.objects.annotate(num_subcategories=Count('subcategory')).filter(num_subcategories__gt=0)
    user = request.user
    cart_instance = Cart(request)
    cart = cart_instance.cart
    cart_count = len(cart)
    shipping = Shipping.objects.last()

    context = {
        "header_category": header_category,
        "cart_count": cart_count,
        "shipping_price": shipping,
    }

    return context

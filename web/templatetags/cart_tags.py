from django import template
from product.models import ProductVariant
from web.cart import Cart  

register = template.Library()

@register.simple_tag(takes_context=True)
def get_carted_quantity(context, product_variant):
    request = context['request']
    cart = Cart(request)
    return cart.get_product_quantity(product_variant)

@register.simple_tag(takes_context=True)
def get_is_product_in_cart(context, product_variant):
    request = context['request']
    cart = Cart(request)
    return cart.is_product_in_cart(product_variant)

    
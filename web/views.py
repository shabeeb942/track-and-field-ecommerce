from typing import Any, Dict
import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404 ,redirect
from django.http import HttpResponse,JsonResponse
from django.urls import reverse
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.generic import View,ListView, DetailView, TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q

from .models import CategoryOffer,Banner,OfferBanner

from product.models import Category, SubCategory, Product ,ProductVariant ,Wishlist,Brand,DealOfTheDay

from .cart import Cart

from accounts.models import User

from order.models import OrderItem,Order
from order.forms import OrderForm
from .forms import ContactForm


client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY, settings.RAZOR_PAY_SECRET))

class Index(TemplateView):
    template_name = "web/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Retrieve products
        context["products"] = Product.objects.filter(is_active=True)
        context["top_selling"] = Product.objects.filter(is_top_selling=True).order_by("?")
        context["popular_products"] = Product.objects.filter(is_popular=True)[:20]
        context["new_products"] = Product.objects.filter(is_new_arrival=True).order_by("?")

        # Retrieve categories and their products
        categories = Category.objects.all()
        category_products = {}
        for category in categories:
            category_products[category] = Product.objects.filter(subcategory__category=category, is_active=True)


        context["category_products"] = category_products
        context["categories"] = categories

        # Retrieve brands
        context["brands"] = Brand.objects.all()

        # Retrieve offers
        context["offers"] = OfferBanner.objects.filter(is_active=True).order_by("?")

        # Retrieve deals of the day
        context["active_deals"] = DealOfTheDay.objects.filter(is_offer_end=False).order_by("?")

        # Retrieve banners
        context["banners"] = Banner.objects.filter(is_active=True)

        # Retrieve category offers
        context["category_offers"] = CategoryOffer.objects.filter(is_active=True).order_by("?")
        # context["popular_products_category"] = CategoryOffer.objects.filter(is_popular=True).order_by("?").last()
        # context["new_products_category"] = CategoryOffer.objects.filter(is_new_arrival=True).order_by("?").last()

        return context

class Search(TemplateView):
    template_name = "web/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Retrieve products
        context["products"] = Product.objects.filter(is_active=True)
        return context


class ProductList(ListView):
    model = Product
    template_name = "web/shop.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        queryset = Product.objects.all()

        # Fetch search query from request
        search_query = self.request.GET.get("search")

        # Filter products by search query if it exists
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))

        # Fetch category and subcategory from request
        category_slug = self.request.GET.get("category")
        subcategory_slug = self.request.GET.get("sub_category")

        # Filter products by category and subcategory if they exist
        if category_slug:
            queryset = queryset.filter(subcategory__category__slug=category_slug)
            self.category_title = Category.objects.get(slug=category_slug)
        else:
            self.category_title = None

        if subcategory_slug:
            queryset = queryset.filter(subcategory__slug=subcategory_slug)
            self.sub_category_title = SubCategory.objects.get(slug=subcategory_slug)
        else:
            self.sub_category_title = None

        # Fetch brand from request
        brand_slug = self.request.GET.get("brand")
        if brand_slug:
            queryset = queryset.filter(brand__slug=brand_slug)
            self.brand_title = Brand.objects.get(slug=brand_slug)
        else:
            self.brand_title = None

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_shop"] = True
        context["categories"] = Category.objects.all()
        context["title"] = self.category_title
        context["subtitle"] = self.sub_category_title
        context["brand_title"] = self.brand_title
        context["brands"] = Brand.objects.all()
        return context



class ProductDetail(DetailView):
    model = Product
    template_name = "web/product-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(is_active=True)
        context["related_products"] = Product.objects.filter(
            subcategory__slug=self.object.subcategory.slug,
            is_active=True
        ).exclude(id=self.object.id)
        return context



# class CartView(TemplateView):
#     template_name = "web/cart.html"


class CheckoutView(View):
    template_name = "web/checkout.html"

    def get(self, request):
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)

        context = {
            'cart_items': cart_items,
            'cart_total': cart.cart_total(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)
        user = request.user

        if form.is_valid():
            order = form.save(commit=False)

            order.user = user if user.is_authenticated else None

            order.payment_method = request.POST.get('paymentMethod')
            order.shipping_fee = request.POST.get('shipping_price')
            order.total = request.POST.get('total_price')
            order.subtotal = order.total
            order.payable = order.total
            order.save()

            for item_id, item_data in cart.get_cart():
                variant = get_object_or_404(ProductVariant, id=item_id)
                quantity = item_data["quantity"]
                price = Decimal(item_data["price"])

                order_item = OrderItem.objects.create(
                    order=order,
                    product=variant,
                    price=price,
                    quantity=quantity,
                )

            if order.payment_method == "OP":
                return redirect("web:payment", pk=order.pk)
            else:
                cart.clear()
                return redirect("web:complete_order", pk=order.pk)

        else:
            print(form.errors)
            context = {
                "cart_items": cart_items,
                "cart_total": sum(item["total_price"] for item in cart_items),
                "form": form,
            }
            return render(request, self.template_name, context)

    def get_cart_items(self, cart):
        cart_items = []
        for item_id, item_data in cart.get_cart():
            variant = get_object_or_404(ProductVariant, id=item_id)
            quantity = item_data['quantity']
            total_price = Decimal(item_data['price']) * quantity

            cart_items.append({
                'product': variant,
                'quantity': quantity,
                'total_price': total_price,
            })
        return cart_items


class PaymentView(View):
    def get(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)
        currency = "INR"
        amount = float(order.payable) * 100
        razorpay_order = client.order.create(
            {"amount": amount, "currency": currency, "payment_capture": "1"}
        )
        razorpay_order_id = razorpay_order["id"]
        order.razorpay_order_id = razorpay_order_id
        order.save()

        context = {
            "object": order,
            "amount": amount,
            "razorpay_key": settings.RAZOR_PAY_KEY,
            "razorpay_order_id": razorpay_order_id,
            "callback_url": f"{settings.DOMAIN}/callback/{order.pk}/",
        }
        return render(request, "web/payment.html", context=context)


@csrf_exempt
def callback(request, pk):
    order = get_object_or_404(Order, pk=pk)
    print(request.GET)
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        response_data = {
            "razorpay_order_id": provider_order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature_id,
        }

        order = Order.objects.get(razorpay_order_id=provider_order_id)
        order.razorpay_payment_id = payment_id
        order.razorpay_signature = signature_id
        client = razorpay.Client(
            auth=(settings.RAZOR_PAY_KEY, settings.RAZOR_PAY_SECRET)
        )
        result = client.utility.verify_payment_signature(response_data)

        if result is not None:
            print("Signature verification successful")
            order.is_ordered = True
            order.order_status = "Placed"
            order.payment_status = "Success"
            order.save()



            print("email sent successfully")
            cart = Cart(request)
            cart.clear()

        else:
            print("Signature verification failed, please check the secret key")
            order.payment_status = "Failed"
            order.save()
        return render(request, "web/callback.html", {"object": order})
    else:
        print("Razorpay payment failed")
        return redirect("web:payment", pk=order.pk)


class CompleteOrderView(DetailView):
    model = Order
    template_name = "web/complete-order.html"

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs["pk"])




class UserOrdersView(TemplateView,LoginRequiredMixin):
    template_name = "web/user-orders.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = Order.objects.filter(user=self.request.user)
        return context


class UserOrderDetailView(DetailView):
    model = Order
    template_name = "web/order_single.html"
    context_object_name = "order"
    slug_field = "order_id"
    slug_url_kwarg = "order_id"
    extra_context = {"my_order": True}

# cart

class CartView(View):
    def get(self, request):
        cart = Cart(request)
        cart_items = []

        for item_id, item_data in cart.get_cart():
            variant = get_object_or_404(ProductVariant, id=item_id)
            quantity = item_data['quantity']
            total_price = Decimal(item_data['price']) * quantity

            cart_items.append({
                'product': variant,
                'quantity': quantity,
                'total_price': total_price,
            })

        context = {
            'cart_items': cart_items,
            'cart_total': cart.cart_total(),
        }
        return render(request, "web/cart.html", context)

class CartAddView(View):
    def get(self, request):
        cart = Cart(request)
        cart_instance = cart.cart
        quantity = request.GET.get('quantity', 1)
        product_id = request.GET.get("product_id", '')
        price = request.GET.get("price", None)
        variant = get_object_or_404(ProductVariant, pk=product_id)
        cart.add(variant, quantity=int(quantity),price=price)


        return JsonResponse({
            'quantity': cart.get_product_quantity(variant),
            'total_price': cart.get_total_price(cart_instance[product_id]),
            'cart_total': cart.cart_total(),
            'cart_count': len(cart_instance),

        })

class CartUpdateView(View):
    def get(self, request):
        # Initialize the cart
        cart = Cart(request)

        # Get the product variant ID and quantity from the request
        product_id = request.GET.get("product_id", '')
        quantity = int(request.GET.get('quantity', 1))
        price = str(request.GET.get('price', None))

        # Retrieve the product variant
        variant = get_object_or_404(ProductVariant, pk=product_id)

        # Update the quantity of the product variant in the cart
        cart.update_quantity(variant, quantity,price)

        # Get updated cart information
        cart_instance = cart.cart
        print('cart instance===', cart_instance)

        # Construct the JSON response
        return JsonResponse({
            'quantity': cart.get_product_quantity(variant),
            'total_price': cart.get_total_price(cart_instance[product_id]),
            'cart_total': cart.cart_total(),
            'cart_count': len(cart_instance),

        })

class ClearCartItemView(View):
    def get(self, request, item_id):
        cart = Cart(request)
        cart_instance = cart.cart

        variant = get_object_or_404(ProductVariant, id=item_id)
        cart.remove(variant)
        return JsonResponse({
            'quantity': cart.get_product_quantity(variant),
            'cart_total': cart.cart_total(),
            'cart_count': len(cart_instance),
            'removed':True

        })


class MinusToCartView(View):
    def get(self, request):
        cart = Cart(request)
        cart_instance = cart.cart
        item_id = request.GET.get("item_id")
        variant = get_object_or_404(ProductVariant, id=item_id)
        cart.decrease_quantity(variant)
        return JsonResponse({
            'quantity':cart.get_product_quantity(variant),
            'total_price': cart.get_total_price(cart_instance[item_id]),
            'cart_total': cart.cart_total(),
        })

class ClearCartView(View):
    def get(self, request):
        cart = Cart(request)
        cart.clear()
        return redirect(reverse('web:shop'))



# whislist

class WishlistListView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = "web/wishlist.html"
    context_object_name = "wishlist_items"

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class AddToWishlistView( View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'User not authenticated'}, status=401)
        user = self.request.user
        product_id = request.GET.get("product_id",'')
        product = get_object_or_404(Product, pk=product_id)
        if not Wishlist.objects.filter(user=user, product=product).exists():
            # Create a new Wishlist object
            Wishlist.objects.create(
                user=user,
                product=product
            )
            return JsonResponse({'message': 'Product Added from Wishlist successfully','wishlist_count':Wishlist.objects.filter(user=request.user).count()})
        else:
            return JsonResponse({'message': 'Product is already in the Wishlist.','alreadyInWishlist': True})


class RemoveFromWishlistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        user = self.request.user

        wishlist_item = get_object_or_404(Wishlist, user=user, id=product_id)
        wishlist_item.delete()

        return redirect("web:wishlist")




def get_price(request):
    user = request.user
    if request.method == 'GET' :
        product_id = request.GET.get('product_id')
        quantity = request.GET.get('quantity')
        print(product_id,quantity)
        try:
            product_variant = ProductVariant.objects.get(id=product_id)
            print(product_variant)
            price = product_variant.get_price_for_quantity(quantity,user)
            return JsonResponse({'price': price})
        except ProductVariant.DoesNotExist:
            return JsonResponse({'error': 'Product variant not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)




from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

@receiver(user_logged_out)
def log_user_logout(sender, user, request, **kwargs):
    print("User logged out:", user.username)


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'web/contact.html'

    def form_valid(self, form):
        form.save()

        data = form.cleaned_data

        message = (
            f'Name: {data["name"]} \n'
            f'Phone: {data["phone"]} \n'
            f'Email: {data["email"]} \n'
            f'Message: {data["message"]} \n'
        )

        whatsapp_api_url = "https://api.whatsapp.com/send"
        phone_number = "+918075029472"
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"{whatsapp_api_url}?phone={phone_number}&text={encoded_message}"

        # Redirect to the WhatsApp link
        return redirect(whatsapp_url)

    def form_invalid(self, form):
        response_data = {"status": "false", "title": "Form validation error"}
        return JsonResponse(response_data, status=400)

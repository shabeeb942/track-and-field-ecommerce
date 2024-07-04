from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from core import mixins
from product.models import Product, Category, SubCategory
from order.models import Order

class HomeView(UserPassesTestMixin, mixins.HybridTemplateView):
    template_name = "core/home.html"

    def test_func(self):
        # Check if the user is a superuser
        return self.request.user.is_superuser

    def handle_no_permission(self):
        # Redirect to login page if the user doesn't pass the test
        return redirect('auth_login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_count"] = Product.objects.all().count()
        context["subcategory_count"] = SubCategory.objects.all().count()
        context["category_count"] = Category.objects.all().count()
        context["order"] = Order.objects.all().order_by("-id")[:20]
        return context

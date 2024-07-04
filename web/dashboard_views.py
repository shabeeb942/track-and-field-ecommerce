from django.urls import reverse_lazy
from .models import Banner,CategoryOffer
from . import tables
from core import mixins
from order.models import Order


# banner
class BannerListView(mixins.HybridListView):
    model = Banner
    table_class = tables.BannerTable
    filterset_fields = ("sub_category",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Banners"
        context["can_add"] = True
        context["new_link"] = reverse_lazy("web:banner_create")
        return context


class BannerDetailView(mixins.HybridDetailView):
    model = Banner

class BannerCreateView(mixins.HybridCreateView):
    model = Banner
    fields = ("image","sub_category")

class BannerUpdateView(mixins.HybridUpdateView):
    model = Banner
    fields = ("image","sub_category")

class BannerDeleteView(mixins.HybridDeleteView):
    model = Banner


# category offer
class CategoryOfferListView(mixins.HybridListView):
    model = CategoryOffer
    table_class = tables.CategoryOfferTable
    filterset_fields = ("category",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Category Offers"
        context["can_add"] = True
        context["new_link"] = reverse_lazy("web:category_offer_create")
        return context


class CategoryOfferDetailView(mixins.HybridDetailView):
    model = CategoryOffer

class CategoryOfferCreateView(mixins.HybridCreateView):
    model = CategoryOffer
    fields = ("image","category","is_active",)

class CategoryOfferUpdateView(mixins.HybridUpdateView):
    model = CategoryOffer
    fields = ("image","category","is_active",)

class CategoryOfferDeleteView(mixins.HybridDeleteView):
    model = CategoryOffer

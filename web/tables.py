from core.base import BaseTable
from .models import Banner,CategoryOffer
from order.models import Order


class BannerTable(BaseTable):
    class Meta:
        model = Banner
        fields = ("image","sub_category")
        attrs = {"class": "table key-buttons border-bottom"}


class CategoryOfferTable(BaseTable):
    class Meta:
        model = CategoryOffer
        fields = ("image","category",)
        attrs = {"class": "table key-buttons border-bottom"}


class OrderTable(BaseTable):
    class Meta:
        model = Order
        fields = ("order_id","full_name","order_status")
        attrs = {"class": "table key-buttons border-bottom"}

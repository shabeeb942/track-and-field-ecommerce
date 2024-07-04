import uuid

from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from core.base import BaseModel


def generate_order_id():
    timestamp = timezone.now().strftime("%y%m%d")
    unique_id = uuid.uuid4().hex[:6]
    return f"{timestamp}{unique_id.upper()}"


class Order(BaseModel):
    unique_transaction_id = models.UUIDField(
        unique=True, editable=False, blank=True, null=True
    )
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payable = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_id = models.CharField(max_length=255, default=generate_order_id)
    is_ordered = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    payment_method = models.CharField(
        max_length=20,
        choices=(("COD", "Cash On Delivery"), ("OP", "Online Payment")),
        default="COD",
    )


    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    full_name = models.CharField(max_length=100)
    address_line_1 = models.CharField("Complete Address", max_length=100)
    address_line_2 = models.CharField("Landmark", max_length=100)
    state = models.CharField(max_length=200, null=True)
    district = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100)
    pin_code = models.IntegerField()
    mobile_no = models.CharField(max_length=15)
    alternative_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_status = models.CharField(
        max_length=50,
        default="Pending",
        choices=(
            ("Pending", "Pending"),
            ("Placed", "Order Placed"),
            ("Shipped", "Order Shipped"),
            ("InTransit", "In Transit"),
            ("Delivered", "Order Delivered"),
            ("Cancelled", "Order Cancelled"),
        ),
    )
    payment_status = models.CharField(
        max_length=50,
        default="Pending",
        choices=(
            ("Pending", "Pending"),
            ("Failed", "Failed"),
            ("Success", "Success"),
            ("Cancelled", "Cancelled"),
        ),
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ("-id",)

    def get_items(self):
        return OrderItem.objects.filter(order=self)

    def get_grand_total(self):
        total = self.payable + self.service_fee + self.shipping_fee
        return total

    def order_total(self):
        return float(sum([item.subtotal() for item in self.get_items()]))


    def get_user_absolute_url(self):
        return reverse("web:order_detail", kwargs={"order_id": self.order_id})

    def get_absolute_url(self):
        return reverse("web:dash_order_detail", kwargs={"pk": self.pk})


    @staticmethod
    def get_list_url():
        return reverse_lazy("web:order_list")

    # def get_update_url(self):
    #     return reverse_lazy("web:order_update", kwargs={"pk": self.pk})

    # def get_delete_url(self):
    #     return reverse_lazy("web:order_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.order_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey("product.ProductVariant", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        return f"{self.order} - {self.product}"

    def subtotal(self):
        return self.price * self.quantity

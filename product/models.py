from django.db import models
from django.urls import reverse_lazy
from tinymce.models import HTMLField
from web.cart import Cart
from accounts.models import User

from colorfield.fields import ColorField


# Create your models here.
from core.base import BaseModel
from django.utils import timezone
from datetime import timedelta


class Category(BaseModel):
    image=models.ImageField(upload_to="category")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    def __str__(self):
        return self.name

    def get_products(self):
        return Product.objects.filter(subcategory__category=self)

    def get_subcategories(self):
        return SubCategory.objects.filter(category=self)

    def get_absolute_url(self):
        return reverse_lazy("product:category_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("product:category_list")

    def get_update_url(self):
        return reverse_lazy("product:category_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("product:category_delete", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ('Categories')


class SubCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("product:subcategory_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("product:subcategory_list")

    def get_update_url(self):
        return reverse_lazy("product:subcategory_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("product:subcategory_delete", kwargs={"pk": self.pk})

    def get_products(self):
        return Product.objects.filter(subcategory=self)

    class Meta:
        verbose_name = ('Sub Category')
        verbose_name_plural = ('Sub Categories')


class Product(BaseModel):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to="product")
    brand = models.ForeignKey("product.Brand", on_delete=models.CASCADE, blank=True, null=True)
    description = HTMLField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_top_selling = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse_lazy("web:product-detail", kwargs={"slug": self.slug})

    def get_absolute_dashboard_url(self):
        return reverse_lazy("product:product_detail", kwargs={"pk": self.pk})

    def get_product_variants(self):
        return ProductVariant.objects.filter(product=self)

    def get_product_variant(self):
        return ProductVariant.objects.filter(product=self).first()

    def get_images(self):
        return ProductImage.objects.filter(product=self)


    def get_min_price(self):
        price=None
        sizes = self.get_product_variants()
        valid_prices = [p.price for p in sizes if p.price is not None]
        if valid_prices:
            price = min(valid_prices)
        return price

    def get_min_price_name(self):
        name=None
        sizes = self.get_product_variants()
        valid_prices = [p.title for p in sizes if p.price is not None]
        if valid_prices:
            name = min(valid_prices)
        return name


    def get_old_price(self):
        sizes = self.get_product_variants()
        valid_prices = [p.old_price for p in sizes if p.old_price is not None]
        return min(valid_prices) if valid_prices else None


    def get_offer_percent_first(self):
        return self.get_product_variants().first().offer_percent()

    def get_offer_percent(self):
        return min([p.offer_percent() for p in self.get_product_variants()])

    def get_price_variants(self):
        price_variants = PriceVariant.objects.filter(product__product=self)
        return price_variants

    @staticmethod
    def get_list_url():
        return reverse_lazy("product:product_list")

    def get_update_url(self):
        return reverse_lazy("product:product_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("product:product_delete", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = ('Product')
        verbose_name_plural = ('Products')

    def __str__(self):
        return self.name




class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="products/", help_text=" The recommended size is 800x600 pixels."
    )

    class Meta:
        verbose_name = ("Product Image")
        verbose_name_plural = ("Product Images")
        ordering = ("product",)

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(ProductImage, self).delete(*args, **kwargs)
        storage.delete(path)


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField("unit", max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.product} - {self.title}"

    def carted_quantity(self, request):
        cart = Cart(request)
        return cart.get_product_quantity(self)

    def offer_percent(self):
        if self.price is None or self.old_price is None:
            return None
        return (self.old_price - self.price) / self.old_price * 100

    def get_saved_price(self):
        if self.price is None or self.old_price is None:
            return None
        return self.old_price - self.price

    def user_price(self, user):
        return self.price

    def get_price_for_quantity(self, quantity, user):
        price_variant = PriceVariant.objects.filter(product=self, quantity__lte=quantity).order_by('-quantity').first()
        if price_variant:
            return price_variant.price
        else:
            return self.price

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField("unit", max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.product} - {self.title}"

    def carted_quantity(self, request):
        cart = Cart(request)
        return cart.get_product_quantity(self)

    def offer_percent(self):
        if self.price is None or self.old_price is None:
            return None
        return (self.old_price - self.price) / self.old_price * 100

    def get_saved_price(self):
        if self.price is None or self.old_price is None:
            return None
        return self.old_price - self.price

    def user_price(self, user):
        return self.price

    def get_price_for_quantity(self, quantity, user):
        price_variant = PriceVariant.objects.filter(product=self, quantity__lte=quantity).order_by('-quantity').first()
        if price_variant:
            return price_variant.price
        else:
            return self.price



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.product}"


class PriceVariant(models.Model):
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.product.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to="brands")

    def __str__(self):
        return self.name


class DealOfTheDay(models.Model):
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    end_time = models.DateTimeField(blank=True, null=True)
    is_offer_end = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("Deal Of The Day")
        verbose_name_plural = ("Deal Of The Days")
        ordering = ("id",)

    def __str__(self):
        return self.product.name

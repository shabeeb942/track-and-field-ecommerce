from django.db import models
from django.urls import reverse_lazy
from core.base import BaseModel


# Create your models here.


class CategoryOffer(BaseModel):
    image = models.ImageField(upload_to="offers")
    category = models.ForeignKey("product.SubCategory", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


    def get_absolute_url(self):
        return reverse_lazy("web:category_offer_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("web:category_offer_list")

    def get_update_url(self):
        return reverse_lazy("web:category_offer_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("web:category_offer_delete", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = ('Offer By Category')
        verbose_name_plural = ('Offer By Categories')

    def __str__(self):
        return self.title



class Banner(BaseModel):
    tag = models.CharField(max_length=100,blank=True,null=True)
    title = models.CharField(max_length=100,blank=True,null=True)
    subtitle = models.CharField(max_length=100,blank=True,null=True)
    image = models.ImageField(upload_to="banner")
    sub_category = models.ForeignKey("product.SubCategory", on_delete=models.CASCADE,blank=True,null=True)

    def get_absolute_url(self):
        return reverse_lazy("web:banner_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("web:banner_list")

    def get_update_url(self):
        return reverse_lazy("web:banner_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("web:banner_delete", kwargs={"pk": self.pk})


    def __str__(self):
        return str(self.image)



class Shipping(BaseModel):
    price=models.FloatField(default=0)

    def __str__(self):
        return str(self.price)


class OfferBanner(BaseModel):
    category = models.ForeignKey("product.SubCategory", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="offers")
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse_lazy("web:offer_banner_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("web:offer_banner_list")

    def get_update_url(self):
        return reverse_lazy("web:offer_banner_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("web:offer_banner_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=120)
    timestamp = models.DateTimeField(db_index=True,auto_now_add=True)
    email = models.EmailField(blank=True,null=True)
    phone = models.CharField(max_length=120,blank=True,null=True)
    message = models.TextField()

    def __str__(self):
        return str(self.name)

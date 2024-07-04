from django.contrib import admin

from .models import CategoryOffer,Banner,Shipping,OfferBanner,Contact
# Register your models here.

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "sub_category")


@admin.register(CategoryOffer)
class CategoryOfferAdmin(admin.ModelAdmin):
    pass

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    pass


@admin.register(OfferBanner)
class OfferBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "category")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone')

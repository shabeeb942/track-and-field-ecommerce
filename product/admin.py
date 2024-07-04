from django.contrib import admin
from .models import Category, SubCategory, Product ,ProductImage ,ProductVariant ,PriceVariant,Brand,DealOfTheDay
# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class PriceVariantInline(admin.TabularInline):
    model = PriceVariant
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_display_links = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_display_links = ("name", "slug")
    list_filter = ("category",)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name",'is_active')
    list_display_links = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("subcategory",'is_active','is_top_selling','is_popular','is_new_arrival')
    inlines=[ProductVariantInline,ProductImageInline]



@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_filter = ("product",)
    search_fields = ("product",)
    inlines=[PriceVariantInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_display_links = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}



@admin.register(DealOfTheDay)
class DealOfTheDayAdmin(admin.ModelAdmin):
    list_display = ("product", "end_time",'is_offer_end')
    list_display_links = ("product", "end_time",'is_offer_end')
    list_filter = ('is_offer_end',)

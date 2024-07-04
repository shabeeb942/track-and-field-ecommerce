from django import forms
from django.forms import inlineformset_factory
from .models import Product,ProductVariant,ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "image",
            "subcategory",
            "name",
            "slug",
            "description",
            "is_active",
            "is_top_selling",
            "is_popular",
            "is_new_arrival",
        )

def create_variant_formset(parent_model, item_model, item_form, can_delete=True):
    return inlineformset_factory(
        parent_model,
        item_model,
        form=item_form,
        extra=1,
        can_delete=can_delete,
    )


class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = (
            "title",
            "price",
            "price",
            "old_price",
        )

ProductVariantFormSet = create_variant_formset(Product, ProductVariant, ProductVariantForm)



def create_image_formset(parent_model, item_model, item_form, can_delete=True):
    return inlineformset_factory(
        parent_model,
        item_model,
        form=item_form,
        extra=1,
        can_delete=can_delete,
    )

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = (
            "image",
        )

ProductImageFormSet = create_image_formset(Product, ProductImage, ProductImageForm)

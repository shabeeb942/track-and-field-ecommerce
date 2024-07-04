from django.db.models import F
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.forms import modelform_factory


from . import tables
from .models import Category,SubCategory,Product
from core import mixins
from .forms import ProductForm,ProductVariantFormSet,ProductImageFormSet



# category

class CategoryListView(mixins.HybridListView):
    model = Category
    table_class = tables.CategoryTable
    filterset_fields = ("name",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Categorys"
        context["can_add"] = True
        context["new_link"] = reverse_lazy("product:category_create")
        return context


class CategoryDetailView(mixins.HybridDetailView):
    model = Category


class CategoryCreateView(mixins.HybridCreateView):
    model = Category
    fields = ("image","name","slug",)


class CategoryUpdateView(mixins.HybridUpdateView):
    model = Category
    fields = ("image","name","slug",)


class CategoryDeleteView(mixins.HybridDeleteView):
    model = Category


# subcategory

class SubCategoryListView(mixins.HybridListView):
    model = SubCategory
    table_class = tables.SubCategoryTable
    filterset_fields = ("name",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sub Categorys"
        context["can_add"] = True
        context["new_link"] = reverse_lazy("product:subcategory_create")
        return context


class SubCategoryDetailView(mixins.HybridDetailView):
    model = SubCategory

class SubCategoryCreateView(mixins.HybridCreateView):
    model = SubCategory
    fields = ("category","name","slug",)

class SubCategoryUpdateView(mixins.HybridUpdateView):
    model = SubCategory
    fields = ("category","name","slug",)

class SubCategoryDeleteView(mixins.HybridDeleteView):
    model = SubCategory


# product

class ProductListView(mixins.HybridListView):
    model = Product
    table_class = tables.ProductTable
    filterset_fields = ("name",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Products"
        context["can_add"] = True
        context["new_link"] = reverse_lazy("product:product_create")
        return context


class ProductDetailView(mixins.HybridDetailView):
    model = Product


class ProductCreateView(mixins.HybridCreateView):
    model = Product
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['variant_formset'] = ProductVariantFormSet(self.request.POST, prefix='variant_set')
            context['image_formset'] = ProductImageFormSet(self.request.POST, self.request.FILES, prefix='image_set')
        else:
            context['variant_formset'] = ProductVariantFormSet(prefix='variant_set')
            context['image_formset'] = ProductImageFormSet(prefix='image_set')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        variant_formset = context['variant_formset']
        image_formset = context['image_formset']
        if variant_formset.is_valid() and image_formset.is_valid():
            self.object = form.save()
            variant_formset.instance = self.object
            variant_formset.save()
            image_formset.instance = self.object
            image_formset.save()
            print("=========================success=========================")
            return super().form_valid(form)
        else:
            print("=========================form invalid=========================")
            print(variant_formset.errors)
            print(image_formset.errors)
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)




class ProductUpdateView(mixins.HybridUpdateView):
    model = Product
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['variant_formset'] = ProductVariantFormSet(self.request.POST, instance=self.object, prefix='variant_set')
            context['image_formset'] = ProductImageFormSet(self.request.POST, self.request.FILES, instance=self.object, prefix='image_set')
        else:
            context['variant_formset'] = ProductVariantFormSet(instance=self.object, prefix='variant_set')
            context['image_formset'] = ProductImageFormSet(instance=self.object, prefix='image_set')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        variant_formset = context['variant_formset']
        image_formset = context['image_formset']
        if variant_formset.is_valid() and image_formset.is_valid():
            self.object = form.save()
            variant_formset.instance = self.object
            variant_formset.save()
            image_formset.instance = self.object
            image_formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)



class ProductDeleteView(mixins.HybridDeleteView):
    model = Product

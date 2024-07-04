from django.urls import path

from . import views


app_name = "product"

urlpatterns = [
    
    # category
    path("category/", views.CategoryListView.as_view(), name="category_list"),
    path("category/<str:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),
    path("new/category/", views.CategoryCreateView.as_view(), name="category_create"),
    path("category/<str:pk>/update/", views.CategoryUpdateView.as_view(), name="category_update"),
    path("category/<str:pk>/delete/", views.CategoryDeleteView.as_view(), name="category_delete"),
    
    # subcategory
    path("subcategory/", views.SubCategoryListView.as_view(), name="subcategory_list"),
    path("subcategory/<str:pk>/", views.SubCategoryDetailView.as_view(), name="subcategory_detail"),
    path("new/subcategory/", views.SubCategoryCreateView.as_view(), name="subcategory_create"),
    path("subcategory/<str:pk>/update/", views.SubCategoryUpdateView.as_view(), name="subcategory_update"),
    path("subcategory/<str:pk>/delete/", views.SubCategoryDeleteView.as_view(), name="subcategory_delete"),
    
    # product
    path("product/", views.ProductListView.as_view(), name="product_list"),
    path("product/<str:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("new/product/", views.ProductCreateView.as_view(), name="product_create"),
    path("product/<str:pk>/update/", views.ProductUpdateView.as_view(), name="product_update"),
    path("product/<str:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),
    
]

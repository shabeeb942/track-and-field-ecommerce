# Create web/urls.py and paste the following
from django.urls import path
from . import views
from . import dashboard_views
from django.views.generic import TemplateView
from order.views import OrderDetailView,OrderListView

app_name = "web"

urlpatterns = [

    path("", views.Index.as_view(), name="index"),
    path("shop/", views.ProductList.as_view(), name="shop"),
    path("product/<slug>/", views.ProductDetail.as_view(), name="product-detail"),

    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("complete-order/<str:pk>/",views.CompleteOrderView.as_view(),name="complete_order"),
    path("order/",views.UserOrdersView.as_view(),name="user_order"),
    path("search/", views.Search.as_view(), name="search"),

    # payment
    path("payment/<str:pk>/", views.PaymentView.as_view(), name="payment"),
    path("callback/<str:pk>/", views.callback, name="callback"),
    path("order/<str:order_id>/detail/",views.UserOrderDetailView.as_view(),name="order_detail"),

    # cart
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart-add/', views.CartAddView.as_view(), name='add_cart'),
    path('cart-update/', views.CartUpdateView.as_view(), name='update_cart'),
    path('cart-item-clear/<str:item_id>/', views.ClearCartItemView.as_view(), name='clear_cart_item'),
    path('cart-minus/', views.MinusToCartView.as_view(), name='minus_to_cart'),
    path('cart-clear/', views.ClearCartView.as_view(), name='clear_cart'),

    #wishlist
    path("wishlist/", views.WishlistListView.as_view(), name="wishlist"),
    path("wishlist/add/",views.AddToWishlistView.as_view(),name="add_to_wishlist"),
    path("wishlist/remove/<int:product_id>/",views.RemoveFromWishlistView.as_view(),name="remove_from_wishlist"),


    # dashboard
    path("banners/", dashboard_views.BannerListView.as_view(), name="banner_list"),
    path("banner/<str:pk>/", dashboard_views.BannerDetailView.as_view(), name="banner_detail"),
    path("new/banner/", dashboard_views.BannerCreateView.as_view(), name="banner_create"),
    path("banner/<str:pk>/update/", dashboard_views.BannerUpdateView.as_view(), name="banner_update"),
    path("banner/<str:pk>/delete/", dashboard_views.BannerDeleteView.as_view(), name="banner_delete"),

    path("category-offer/",dashboard_views.CategoryOfferListView.as_view(),name="category_offer_list"),
    path("category-offer/<str:pk>/",dashboard_views.CategoryOfferDetailView.as_view(),name="category_offer_detail"),
    path("new/category-offer/",dashboard_views.CategoryOfferCreateView.as_view(),name="category_offer_create"),
    path("category-offer/<str:pk>/update/",dashboard_views.CategoryOfferUpdateView.as_view(),name="category_offer_update"),
    path("category-offer/<str:pk>/delete/",dashboard_views.CategoryOfferDeleteView.as_view(),name="category_offer_delete"),

    path("all-order/",OrderListView.as_view(),name="order_list"),
    path("order-detail/<str:pk>/",OrderDetailView.as_view(),name="dash_order_detail"),

    path('get_price/',views.get_price, name='get_price'),

    # Policies
    path("privacy-policy/", TemplateView.as_view(template_name="web/privacy-policy.html"),name='privacy-policy'),
    path("refund-policy/", TemplateView.as_view(template_name="web/refund-policy.html"),name='refund-policy'),
    path("shipping-policy/", TemplateView.as_view(template_name="web/shipping-policy.html"),name='shipping-policy'),
    path("contact-policy/", TemplateView.as_view(template_name="web/contact-policy.html"),name='contact-policy'),
    path("terms-conditions/", TemplateView.as_view(template_name="web/terms-conditions.html"),name='terms-conditions'),

    path("404/", TemplateView.as_view(template_name="web/404.html"),name='404'),
    path('contact/',views.ContactView.as_view() ,name='contact'),

]

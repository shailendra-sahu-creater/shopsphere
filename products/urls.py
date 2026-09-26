from django.urls import path
from .views import home
from . import views


urlpatterns = [
    path("", home, name="home"),
    path("products/", views.product, name="products"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order-success/", views.order_success, name="order_success"),
    path("products/<int:id>/", views.product_detail, name="product_detail"),
    path("orders/", views.orders, name="orders"),
    path("orders/<int:id>/", views.order_detail, name="order_detail"),
    path("orders/<int:id>/cancel/", views.cancel_order, name="cancel_order"),
]

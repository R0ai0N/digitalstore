from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page_view, name='main'),
    path('category/<slug:slug>/', ProductByCategory.as_view(), name='category'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product'),
    path('search/', search_products_view, name='search'),
    path('login/', login_user_view, name='login'),
    path('registration/', register_user_view, name='registration'),
    path('logout/', logout_user_view, name='logout'),
    path('action/favorite/', action_favorite, name='action_fav'),
    path('favorites/', favorites_view, name='favorites'),
    path('sale/', sale_products_view, name='sale'),
    path('action/basket/', action_basket_customer, name='action_basket'),
    path('cart/', customer_basket_view, name='cart'),
    path('cart/clear/', clear_basket_view, name='clear_cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('payment/', create_checkout_session, name='payment'),
    path('success/', success_payment_view, name='success'),
    path('profile/', profile_customer, name='profile'),
]

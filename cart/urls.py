from django.urls import path
from .views import (
    ItemsView,
    ItemDetailView,
    add_to_cart,
    remove_from_cart,
    OrderSummaryView,
    CheckoutView,
    PaymentView,
    payment_success,
    payment_failure,
    Order_tracking,
    CategoryView,
    Allproducts,
    other_items,
    search,
    ContactView,
    contact_success,
    tailoring,
    about_us,
    faqs,
    Hometest
)


app_name = 'cart'

urlpatterns = [
    path('',ItemsView.as_view(), name = 'item-list'),
    path('checkout/', CheckoutView.as_view(), name = 'checkout'),
    path('product/<slug>/', ItemDetailView.as_view(), name = 'product'),
    path('s/', search, name = 'search'),
    path('add-to-cart/<slug>/', add_to_cart, name = 'add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name = 'remove-from-cart'),
    path('order-summary/',OrderSummaryView.as_view(), name = 'order-summary'),
    path('Allproducts', Allproducts.as_view(), name = 'Allproducts' ),
    path('other-items', other_items.as_view(), name = 'other-items'),
    path('category/<str:cats>',CategoryView, name='category'),
    path('category/Sarees',CategoryView, name='category_sarees'),
    path('category/Dress-materials', CategoryView, name='category_dresses'),
    path('category/Tops', CategoryView, name='category_tops'),
    path('category/Nighties', CategoryView, name='category_nighties'),
    path('contact',ContactView.as_view(),name='contact'),
    path('contact_success',contact_success,name='contact_success'),
    path('tailoring',tailoring,name='tailoring'),
    path('About_us',about_us,name='about_us'),
    path('FAQs',faqs,name = 'faqs'),
    path('payment_success',payment_success,name = 'payment_success'),
    path('payment_failure',payment_failure,name = 'payment_failure'),
    path('payment',PaymentView.as_view(),name = 'payment'),
    path('order_tracking',Order_tracking,name = 'order_tracking' ),

    #Testing view of Homepage
    path('hometest',Hometest, name = 'hometest')
]



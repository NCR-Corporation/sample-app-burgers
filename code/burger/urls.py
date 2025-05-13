from django.urls import path
from burger import views

urlpatterns = [

    path('', views.index, name='index'),
    path('Menu/<str:location>/Lunch', views.lunchMenu, name='lunchMenu'),
    path('Menu/<str:location>/Dinner', views.dinnerMenu, name='dinnerMenu'),
    path('Menu/ItemDetails/<str:itemId>/<str:tag>',
         views.itemDetails, name="itemDetails"),
    path('location', views.location, name='location'),
    path('payment/', views.payment, name='payment'),
    path('ViewCart', views.viewCart, name='viewCart'),
    path('Confirmation', views.confirmation, name='confirmation'),
    path('liveliness', views.liveliness, name="liveliness"),
    path('api/checkout', views.process_checkout, name='process-checkout'),
]

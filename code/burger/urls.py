from django.urls import path
from burger import views

urlpatterns = [

    path('', views.index, name='index'),
    path('menu', views.menu, name='menu'),
    path('itemDetails/<str:location>/<str:time>/<str:tag>/<str:itemId>',
         views.itemDetails, name="itemDetails"),
    path('location', views.location, name='location'),
    path('payment/', views.payment, name='payment'),
    path('viewCart', views.viewCart, name='viewCart'),
    path('confirmation', views.confirmation, name='confirmation'),
    path('liveliness', views.liveliness, name="liveliness"),
]

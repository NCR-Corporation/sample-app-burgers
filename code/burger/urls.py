from django.urls import path
from burger import views

urlpatterns = [

    path('', views.index, name='index'),
    path('findRestaurant', views.findRestaurant, name='findRestaurant'),
    path('midtownMenu', views.midtownMenu, name='midtownMenu'),
    path('southlandMenu', views.southlandMenu, name='southlandMenu'),
    path('highlandsMenu', views.highlandsMenu, name='highlandsMenu'),
    path('payment/', views.payment, name='payment'),
    path('viewCart', views.viewCart, name='viewCart'),
    path('confirmation', views.confirmation, name='confirmation'),
]

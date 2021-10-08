from django.urls import path
from burger import views

urlpatterns = [

    path('', views.index, name='index'),
    path('menu/<str:location>/Lunch', views.lunchMenu, name='lunchMenu'),
    path('menu/<str:location>/Dinner', views.dinnerMenu, name='dinnerMenu'),
    path('menu/itemDetails/<str:itemId>/<str:tag>',
         views.itemDetails, name="itemDetails"),
    path('location', views.location, name='location'),
    path('payment/', views.payment, name='payment'),
    path('viewCart', views.viewCart, name='viewCart'),
    path('confirmation', views.confirmation, name='confirmation'),
    path('liveliness', views.liveliness, name="liveliness"),
]

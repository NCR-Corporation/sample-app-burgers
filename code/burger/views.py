from django.shortcuts import render

# Create your views here.

import http.client
import requests
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
import auxMethods
import catalogMaker
from rest_framework.views import APIView
from rest_framework.decorators import api_view

HIGHLANDS = settings.LOCATIONS['Burgers Unlimited Highlands']
SOUTHLAND = settings.LOCATIONS['Burgers Unlimited Southland']
MIDTOWN = settings.LOCATIONS['Burgers Unlimited Midtown']


def index(request):
    results = auxMethods.findResturantsInRange({'x': -84.38879, 'y': 33.777714}, 20)
    sites = []

    for i in range (0,3):
        sites.append(results[i])
    
    context = {
        'results': sites
    }
    return render(request, 'index.html', context)


def findRestaurant(request):
    address = request.POST['address']
    radius = int(request.POST['radius'])

    coordinates = auxMethods.geoCodeAddress(address)

    if coordinates is None:
        return render(request, 'addressNotFound.html')

    results = auxMethods.findResturantsInRange(coordinates, radius)
    context = {'address': address, "radius": radius,
               'coordinates': coordinates, 'results': results}

    return render(request, 'findRestaurant.html', context)


def midtownMenu(request):
    try:
        items = catalogMaker.getStoreItems('BurgersUnlimitedMidtown')
        items_prices = catalogMaker.getAllPrices(items, MIDTOWN)
    except:
        return render(request, 'error.html')
    context = {'items': items_prices}

    return render(request, 'midtownMenu.html', context)


def southlandMenu(request):
    try:
        items = catalogMaker.getStoreItems('BurgersUnlimitedSouthland')
        items_prices = catalogMaker.getAllPrices(items, SOUTHLAND)
    except:
        return render(request, 'error.html')
    context = {'items': items_prices}

    return render(request, 'southlandMenu.html', context)


def highlandsMenu(request):
    try:
        items = catalogMaker.getStoreItems('BurgersUnlimitedHighlands')
        items_prices = catalogMaker.getAllPrices(items, HIGHLANDS)
    except:
        return render(request, 'error.html')
    context = {'items': items_prices}

    return render(request, 'highlandsMenu.html', context)


def payment(request):
    return render(request, 'payment.html')


def viewCart(request):
    return render(request, 'viewCart.html')


def confirmation(request):

    userCart = request.POST.getlist('cart')


    context = {'cart': userCart}

    return render(request, 'confirmation.html', context)


def about(request):
    return render(request, 'about.html')

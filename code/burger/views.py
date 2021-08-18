from django.shortcuts import render
import re
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
import auxMethods
import catalogMaker
from rest_framework.views import APIView
from rest_framework.decorators import api_view

HIGHLAND = settings.LOCATIONS['Peachtree Burger Highland']
SOUTHLAND = settings.LOCATIONS['Peachtree Burger Southland']
MIDTOWN = settings.LOCATIONS['Peachtree Burger Midtown']

MENUMAPPINGS = {
    'highlandLunch': '1626399748035',
    'highlandDinner': '1628539739497',
    'midtownLunch': '1628542092992',
    'midtownDinner': '1628558391854',
    'southlandLunch': '1628508502301',
    'southlandDinner': '1628508515030'
}

RESULTS = auxMethods.findResturantsInRange(
    {'x': -84.38879, 'y': 33.777714}, 20)
MATCHES = auxMethods.getPeachtreeRestaurants(RESULTS)


def index(request):
    context = {
        'locations': MATCHES
    }
    return render(request, 'index.html', context)


def findRestaurant(request):
    address = request.POST['address']
    radius = int(request.POST['radius'])

    coordinates = auxMethods.geoCodeAddress(address)

    if coordinates is None:
        return render(request, 'addressNotFound.html')

    results = auxMethods.findResturantsInRange(coordinates, radius)
    matches = auxMethods.getPeachtreeRestaurants(results)
    context = {'address': address, "radius": radius,
               'coordinates': coordinates, 'results': results, 'locations': matches}

    return render(request, 'findRestaurant.html', context)


def midtownMenu(request):
    try:
        items = catalogMaker.getStoreItems('BurgersUnlimitedMidtown')
        items_prices = catalogMaker.getAllPrices(items, MIDTOWN)
    except:
        return render(request, 'error.html')

    context = {
        'items': items_prices,
        'locations': MATCHES
    }

    return render(request, 'midtownMenu.html', context)


def southlandMenu(request):
    try:
        items = catalogMaker.getStoreItems('BurgersUnlimitedSouthland')
        items_prices = catalogMaker.getAllPrices(items, SOUTHLAND)
    except:
        return render(request, 'error.html')

    context = {
        'items': items_prices,
        'locations': MATCHES
    }

    return render(request, 'southlandMenu.html', context)


def highlandsMenu(request):
    try:
        items = catalogMaker.getStoreItems('BurgersUnlimitedHighlands')
        items_prices = catalogMaker.getAllPrices(items, HIGHLAND)
    except:
        return render(request, 'error.html')

    context = {
        'items': items_prices,
        'locations': MATCHES
    }

    return render(request, 'highlandsMenu.html', context)


def payment(request):
    context = {'locations': MATCHES}
    return render(request, 'payment.html', context)


def viewCart(request):
    context = {'locations': MATCHES}
    return render(request, 'viewCart.html', context)


def confirmation(request):
    userCart = request.POST.getlist('cart')
    context = {
        'cart': userCart,
        'locations': MATCHES
    }

    return render(request, 'confirmation.html', context)

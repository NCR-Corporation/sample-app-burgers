from menuParser import menuParsing
from HMACAuth import HMACAuth
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
import json

#HIGHLANDS = settings.LOCATIONS['Burgers Unlimited Highlands']
#SOUTHLAND = settings.LOCATIONS['Burgers Unlimited Southland']
#MIDTOWN = settings.LOCATIONS['Burgers Unlimited Midtown']
HIGHLANDS = settings.LOCATIONS['Peachtree Burger Highland']
SOUTHLAND = settings.LOCATIONS['Peachtree Burger Southland']
MIDTOWN = settings.LOCATIONS['Peachtree Burger Midtown']



def index(request):
    return render(request, 'index.html')


'''def findRestaurant(request):
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

    return render(request, 'highlandsMenu.html', context)'''


def highlandsLunch(request):

    try:
        url = 'https://gateway-staging.ncrcloud.com/menu/v2/menu-details/1626399748035'
        conn = requests.get(url,auth=(HMACAuth(HIGHLANDS)))
        
        results = menuParsing(conn.json())
        #print(results)

        return HttpResponse (results)
       

    except:
        return HttpResponse ("Error")




def highlandsDinner(request):
    return HttpResponse ("Highlands Dinner Menu")

'''
def midtownLunch(request):
    return HttpResponse ("Midtown Lunch Menu")

def midtownDinner(request):
    return HttpResponse ("Midtown Dinner Menu")

def southlandLunch(request):
    return HttpResponse ("Southland Lunch Menu")

def southlandDinner(request):
    return HttpResponse ("Southland Dinner Menu")            

'''

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

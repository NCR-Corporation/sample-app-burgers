from menuParser import menuParsing
from HMACAuth import HMACAuth
from django.shortcuts import render

# Create your views here.

import requests
from django.http import HttpResponse
from django.conf import settings
import datetime
import json
import auxMethods


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

site = ''


def index(request):
    results = auxMethods.findResturantsInRange(
        {'x': -84.38879, 'y': 33.777714}, 20)
    sites = []

    for i in range(0, 3):
        sites.append(results[i])

    context = {
        'results': sites
    }

    time = datetime.datetime.now()
    hour = time.hour
    min = time.minute / 100
    hourAndTime = hour + min
    if 15.01 < hourAndTime < 23.59:
        request.session['time'] = 'Dinner'
    else:
        request.session['time'] = 'Lunch'

    return render(request, 'index.html', context)


def menu(request):
    time = request.session.get('time')
    menustring = site+time
    menuMapping = MENUMAPPINGS[menustring]

    url = f'https://gateway-staging.ncrcloud.com/menu/v2/menu-details/{menuMapping}'

    if site == 'highlands':
        conn = requests.get(url, auth=(HMACAuth(HIGHLAND)))
    elif site == 'midtown':
        conn = requests.get(url, auth=(HMACAuth(MIDTOWN)))
    else:
        conn = requests.get(url, auth=(HMACAuth(SOUTHLAND)))

    results = menuParsing(conn.json())
    request.session[f'{location}{time}'] = results
    context = {'items': results, 'time': time, 'site': site}

    return render(request, 'menu.html', context)


def location(request):
    if request.method == 'POST':
        global site
        body = json.loads(request.body)
        site = body['Site']
        print(f'Site Selction:{site}')

    return HttpResponse()


def itemDetails(request, itemId, location, tag, time):
    menu = None
    context = None

    if time == 'lunch':
        if location == 'highland':
            menu = request.session.get('highlandLunch')
        elif location == 'midtown':
            menu = request.session.get('midtownLunch')
        else:
            menu = request.session.get('southlandLunch')
    else:
        if location == 'highland':
            menu = request.session.get('highlandDinner')
        elif location == 'midtown':
            menu = request.session.get('midtownDinner')
        else:
            menu = request.session.get('southlandDinner')

    length = len(menu[tag])
    for item in range(length):

        if menu[tag][item]['id'] == int(itemId):
            context = {'item': menu[tag][item]}

    return render(request, 'itemDetails.html', context)


def payment(request):
    return render(request, 'payment.html')


def viewCart(request):
    return render(request, 'viewCart.html')


def confirmation(request):
    userCart = request.POST.getlist('cart')
    context = {'cart': userCart}

    return render(request, 'confirmation.html', context)

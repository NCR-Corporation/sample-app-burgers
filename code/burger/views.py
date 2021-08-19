from menuParser import menuParsing
from HMACAuth import HMACAuth
from django.shortcuts import render
import datetime
import json
import catalogMaker
import requests
from requests.auth import HTTPBasicAuth
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

RESULTS = auxMethods.findResturantsInRange(
    {'x': -84.38879, 'y': 33.777714}, 20)
MATCHES = auxMethods.getPeachtreeRestaurants(RESULTS)

site = ''


def index(request):
    context = {
        'locations': MATCHES
    }

    time = datetime.datetime.now().hour
    if time > 14:
        request.session['time'] = 'Dinner'
    else:
        request.session['time'] = 'Lunch'

    return render(request, 'index.html', context)


def menu(request):
    time = request.session.get('time')
    menustring = site+time

    if menustring in MENUMAPPINGS:
        menuMapping = MENUMAPPINGS[menustring]
    else:
        return render(request, 'error.html')

    url = f'https://gateway-staging.ncrcloud.com/menu/v2/menu-details/{menuMapping}'

    if site == 'highlands':
        conn = requests.get(url, auth=(HMACAuth(HIGHLAND)))
    elif site == 'midtown':
        conn = requests.get(url, auth=(HMACAuth(MIDTOWN)))
    elif site == 'southland':
        conn = requests.get(url, auth=(HMACAuth(SOUTHLAND)))

    results = menuParsing(conn.json())
    request.session[menustring] = results
    context = {'items': results, 'time': time,
               'site': site, 'locations': MATCHES}
    return render(request, 'menu.html', context)


def location(request):
    if request.method == 'POST':
        global site
        body = json.loads(request.body)
        site = body['Site']

    return HttpResponse()


def itemDetails(request, itemId, location, tag, time):
    menu = None
    context = None

    if time == 'Lunch':
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
            context = {
                'item': menu[tag][item],
                'locations': MATCHES
            }

    return render(request, 'itemDetails.html', context)


def payment(request):
    context = {'locations': MATCHES}
    return render(request, 'payment.html', context)


def viewCart(request):
    context = {'locations': MATCHES}
    return render(request, 'viewCart.html', context)


def confirmation(request):
    userCart = request.POST.getlist('cart')

    context = {'cart': userCart}

    return render(request, 'confirmation.html', context)

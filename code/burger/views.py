from django.http.response import HttpResponseNotAllowed
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
    'highlandLunch': '1631732419306',
    'highlandDinner': '1631649497940',
    'midtownLunch': '1631732484915',
    'midtownDinner': '1631732451617',
    'southlandLunch': '1631732514361',
    'southlandDinner': '1631732546628'
}

RESULTS = auxMethods.findResturantsInRange(
    {'x': -84.38879, 'y': 33.777714}, 20)
MATCHES = auxMethods.getPeachtreeRestaurants(RESULTS)

site = ''


def index(request):
    request.session['location'] = 'Midtown'
    site = request.session['location']
    context = {
        'locations': MATCHES,
        'site': site
    }

    time = datetime.datetime.now().hour
    if time > 14:
        request.session['time'] = 'Dinner'
    else:
        request.session['time'] = 'Lunch'

    return render(request, 'index.html', context)


def lunchMenu(request, location):
    request.session['location'] = location

    time = "Lunch"
    site = request.session.get('location')

    menustring = site.lower()+time

    if menustring in MENUMAPPINGS:
        menuMapping = MENUMAPPINGS[menustring]
    else:
        return render(request, 'error.html')

    url = 'https://api.ncr.com/menu/v2/menu-details/' + menuMapping

    if site == 'Highland':
        conn = requests.get(url, auth=(HMACAuth(HIGHLAND)))
    elif site == 'Midtown':
        conn = requests.get(url, auth=(HMACAuth(MIDTOWN)))
    elif site == 'Southland':
        conn = requests.get(url, auth=(HMACAuth(SOUTHLAND)))

    results = menuParsing(conn.json())

    request.session[menustring] = results

    context = {'items': results, 'time': time,
               'site': site, 'locations': MATCHES}

    return render(request, 'menu.html', context)


def dinnerMenu(request, location):
    request.session['location'] = location

    time = "Dinner"
    site = request.session.get('location')

    menustring = site.lower()+time

    if menustring in MENUMAPPINGS:
        menuMapping = MENUMAPPINGS[menustring]
    else:
        return render(request, 'error.html')

    url = 'https://api.ncr.com/menu/v2/menu-details/' + menuMapping

    if site == 'Highland':
        conn = requests.get(url, auth=(HMACAuth(HIGHLAND)))
    elif site == 'Midtown':
        conn = requests.get(url, auth=(HMACAuth(MIDTOWN)))
    elif site == 'Southland':
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
                'locations': MATCHES,
                'menu': menu,
                'menuLink': '/burger/menu/' + location.capitalize() + '/' + time
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


def liveliness(request):
    return HttpResponse("OK")

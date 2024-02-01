from django.http.response import HttpResponseNotAllowed
from menuParser import menuParsing
from HMACAuth import HMACAuth
from django.shortcuts import render
import datetime
import json
import requests
from django.http import HttpResponse
from django.conf import settings
import datetime
import json
import auxMethods

HIGHLAND = settings.LOCATIONS['Peachtree Burger Highland']
SOUTHLAND = settings.LOCATIONS['Peachtree Burger Southland']
MIDTOWN = settings.LOCATIONS['Peachtree Burger Midtown']

print('HIGHLAND',HIGHLAND)
print('SOUTHLAND',SOUTHLAND)
print('MIDTOWN',MIDTOWN)

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

MENULINK = '/Peachtree-Burger/menu/'
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
    print('lunchRequest', request)
    print('lunchLocation', location)
    request.session['location'] = location

    time = "Lunch"
    request.session['time'] = "Lunch"
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

    request.session.save()
    return render(request, 'menu.html', context)


def dinnerMenu(request, location):
    print('dinnerRequest', request)
    print('DinnerRequestSession0',request.session.get('location'))
    print('dinnerLocation', location)
    request.session['location'] = location

    time = "Dinner"
    request.session['time'] = "Dinner"
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

    print('DinnerRequestSession1',request.session.get('location'))
    print('DinnerRequestSession2',request.session.get('location'))

    response = render(request, 'menu.html', context)
    response.set_cookie('location', location, 300)
    return response


def location(request):
    if request.method == 'POST':
        global site
        body = json.loads(request.body)
        site = body['Site']

    return HttpResponse()


def itemDetails(request, itemId, tag):
    menu = None
    context = None

    print('ItemrequestSession', request.session.get('location'))
    print('request', request)
    print('itemId', itemId)
    print('tag', tag)

    loc = request.COOKIE.get('location')
    print('loc', loc)

    location = request.session.get('location').lower()
    time = request.session.get('time')

    print('location', location)

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
        elif request.session.get('location').lower() == 'midtown':
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
                'menuLink': '/Peachtree-Burger/Menu/' + location.capitalize() + '/' + time
            }

    print('request2', request)
    print('context', context)

    return render(request, 'itemDetails.html', context)


def payment(request):
    context = {'locations': MATCHES}
    return render(request, 'payment.html', context)


def viewCart(request):
    location = request.session.get('location')
    time = request.session.get('time')
    total = request.session.get('Total')

    print('viewCart', location)

    cart = None

    if request.is_ajax() and request.POST.get('cart', None) != None:
        request.session['cart'] = request.POST.get('cart', None)

    if request.session.get('cart') == "":
        cart = None
    elif request.session.get('cart') != None:
        cart = json.loads(request.session.get('cart'))
        cart = json.loads(cart)

    results = []
    toppingColumns = ""
    if cart != None:
        for items in cart:
            if len(items['toppings']) % 4 == 0:
                for numCols in range(int(len(items['toppings']) / 4)):
                    toppingColumns += "a"
            else:
                for numCols in range(int(len(items['toppings']) / 4 + 1)):
                    toppingColumns += "a"

            iteminfo = {
                'id': items['id'],
                'image': items['image'],
                'displayName': items['displayName'],
                'description': items['description'],
                'price': items['price'],
                'tags': items['tags'],
                'toppings': items['toppings'],
                'quantity': items['quantity'],
                'toppingColumns': toppingColumns
            }
            toppingColumns = ""
            results.append(iteminfo)

    context = {
        'locations': MATCHES,
        'cart': results,
        'total': total,
        'menuLink': '/Peachtree-Burger/Menu/' + location.capitalize() + '/' + time
    }

    print('Cartrequest2', request)
    print('Cartcontext', context)

    return render(request, 'viewCart.html', context)


def confirmation(request):
    request.session['cart'] = ""
    request.session['total'] = ""

    return render(request, 'confirmation.html')


def liveliness(request):
    return HttpResponse("OK")

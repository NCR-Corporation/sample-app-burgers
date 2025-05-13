from menuParser import menuParsing
from HMACAuth import HMACAuth
from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.conf import settings
import datetime
import auxMethods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
import json
from order import createOrder
from order import create_order_from_cart
from django.http import HttpResponse
import traceback

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

MENULINK = '/Peachtree-Burger/menu/'
site = ''

def index(request):
    auxMethods.findResturantsInRange(
        {'x': -84.38879, 'y': 33.777714}, 20)
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
    if not request.session.session_key:
        request.session.save()

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

    return render(request, 'menu.html', context)


def location(request):
    if request.method == 'POST':
        global site
        body = json.loads(request.body)
        site = body['Site']

    return HttpResponse()


def itemDetails(request, itemId, tag):
    menu = None
    context = None
    location =  request.session.get('location').lower()
    time = request.session.get('time')

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

    return render(request, 'itemDetails.html', context)


def payment(request):
    context = {'locations': MATCHES}
    return render(request, 'payment.html', context)


def viewCart(request):
    try:
        print("location:", request.session.get('location'))
        print("time:", request.session.get('time'))
        print("cart (raw):", request.session.get('cart'))

        location = request.session.get('location')
        time = request.session.get('time')
        total = request.session.get('Total')

        cart = None

        if request.is_ajax() and request.POST.get('cart', None) != None:
            request.session['cart'] = request.POST.get('cart', None)

        if request.session.get('cart'):
            try:
                cart = json.loads(request.session['cart'])  # decode only once
            except json.JSONDecodeError as e:
                print(f"[ERROR] Failed to decode cart: {e}")
                cart = None

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

        return render(request, 'viewCart.html', context)

    except Exception as e:
        print("❌ Unexpected error in viewCart:")
        traceback.print_exc()
        return HttpResponse("Internal Server Error in viewCart", status=500)

def confirmation(request):
    raw_cart = request.session.get("cart", "[]")

    try:
        cart = json.loads(raw_cart) if isinstance(raw_cart, str) else raw_cart
    except Exception as e:
        print(f"[ERROR] Failed to parse cart from session: {e}")
        cart = []

    location = request.session.get("location", "")

    if cart:
        try:
            order_id = create_order_from_cart(cart, location)
            print(f"[SUCCESS] Order placed. Order ID: {order_id}")
            request.session['order_id'] = order_id
        except Exception as e:
            print(f"[ERROR] Order placement failed: {e}")
    else:
        print("[WARN] Cart was empty. No order created.")

    return render(request, 'confirmation.html')

def liveliness(request):
    return HttpResponse("OK")

@csrf_exempt
def process_checkout(request):
    if request.method == "POST":
        try:
            cart = json.loads(request.body)
            order_id = createOrder(cart)
            return JsonResponse({"orderId": order_id})
        except Exception as e:
            return HttpResponseBadRequest(f"Checkout failed: {str(e)}")
    return HttpResponseBadRequest("Only POST allowed")

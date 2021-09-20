from django.conf import settings
import requests
import json
from HMACAuth import HMACAuth
import re


def geoCodeAddress(address):
    try:
        url = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress'

        payload = {'address': address,
                   'benchmark': 'Public_AR_Current', 'format': 'json'}

        r = requests.get(url, params=payload)
        temp = r.json()

        rjson = json.dumps(temp)
        rjson = json.loads(rjson)
        result = rjson['result']['addressMatches'][0]['coordinates']
    except IndexError:
        print("Address could not be found")
    else:

        return result


def findResturantsInRange(coordinates, radius):
    meters = 1609
    y = coordinates['y']
    x = coordinates['x']
    circle = radius * meters

    url = 'https://api.ncr.com/site/sites/find-nearby/%s,%s' % (
        coordinates['y'], coordinates['x'])

    payload = {
        'numSites': 10,
        'radius': circle,
    }

    r = requests.get(url, params=payload, auth=(HMACAuth()))

    temp = r.json()
    rjson = json.dumps(temp)
    rjson = json.loads(rjson)

    sites = []

    for site in rjson['sites']:
        sites.append(site)

    return sites


def getPeachtreeRestaurants(request):
    siteNames = []
    for i in range(0, len(request)):
        currentSiteName = re.sub(r"\W+", ' ', request[i].get('siteName'))
        if currentSiteName.strip() == 'Peachtree Burger Midtown' or currentSiteName.strip() == 'Peachtree Burger Southland' or currentSiteName.strip() == 'Peachtree Burger Highland':
            siteNames.append(request[i])

    return siteNames


dict = {
    'x': '-84.3895',
    'y': '33.7891',

}
rad = 15

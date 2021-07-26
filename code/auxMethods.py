from django.conf import settings
import requests
import json
from HMACAuth import HMACAuth


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
    # The radius in this function is in meters, so unit that user enters needs to be converted to from miles to meters
    meters = 1609
    y = coordinates['y']
    x = coordinates['x']
    circle = radius * meters

    url = 'https://gateway-staging.ncrcloud.com/site/sites/find-nearby/%s,%s' % (
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


dict = {
    'x': '-84.3895',
    'y': '33.7891',
}
rad = 15

#geoCodeAddress('864 Spring St Nw, Atlanta, GA')

#results =findResturantsInRange(dict,rad)

# print(results)

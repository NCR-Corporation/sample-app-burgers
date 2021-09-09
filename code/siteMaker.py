from django.conf import settings
import requests
from BurgersUnlimited.settings import *
from HMACAuth import HMACAuth

"""
Description: This function creates new sites on the NCR Platform
Parameters: (In Progress) A dictionary of the values that a user would like to be added to a new site
Returns: Nothing. (In Future) A Json confirming the creation of the site. Currently using print statements.

"""


def create(siteName, enterpriseUnitName):
    url = 'https://gateway-staging.ncrcloud.com/site/sites'
    payload = "{\"siteName\":\"%s\",\"enterpriseUnitName\":\"%s\",\"coordinates\":{\"latitude\":33.6817952,\"longitude\":-84.4239568},\"status\":\"ACTIVE\"}" % (
        siteName, enterpriseUnitName)

    r = requests.post(url, payload, auth=(HMACAuth()))


"""
Description: This function allows a user to query the NCR Platform to locate all the sites for the given nep-organization.
Parameters: None
Returns: A json of the nep-organization data
"""


def queryAll():
    url = 'https://gateway-staging.ncrcloud.com/site/sites/find-by-criteria?pageSize=10000'
    payload = "{\"criteria\":{\"status\": \"ACTIVE\"}}"
    request = requests.post(url, payload, auth=(HMACAuth()))
    return request.json()


"""
Description: This function allows a user to query the NCR Platform to locate a particular site,
Parameters: [string] siteId- the alphanumeric string representing the site. NOT the name of the site.
Returns: A json containing the information about the request statement. Currently using print statements.
"""


def queryById(id):
    url = 'https://gateway-staging.ncrcloud.com/site/sites/%s' % id
    request = requests.get(url, auth=(HMACAuth()))
    return request.json()


"""
Description: This function allows a user to update a particular site on the NCR Platform.
Parameters: [string] siteId- the alphanumeric string representing the site. NOT the name of the site.
            [string] name - the new name of the site
Returns: A json containing the information about the updated site.
"""


def update(id, siteName):
    url = 'https://gateway-staging.ncrcloud.com/site/sites/%s' % id
    payload = "{\"siteName\":\"%s\",\"enterpriseUnitName\":\"%s\",\"coordinates\":{\"latitude\":33.6407,\"longitude\":-84.4277},\"status\":\"ACTIVE\"}" % (
        siteName, siteName)
    request = requests.put(url, payload, auth=(HMACAuth()))
    return request.json()


def delete(id, siteName):
    url = 'https://gateway-staging.ncrcloud.com/site/sites/%s' % id
    payload = "{\"siteName\":\"%s\",\"enterpriseUnitName\":\"%s\",\"coordinates\":{\"latitude\":33.6407,\"longitude\":-84.4277},\"status\":\"INACTIVE\"}" % (
        siteName, siteName)
    request = requests.put(url, payload, auth=(HMACAuth()))
    return request.json()

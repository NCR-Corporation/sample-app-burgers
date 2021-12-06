from django.conf import settings
import requests
import re
from BurgersUnlimited import settings
from HMACAuth import HMACAuth

HIGHLANDS = settings.LOCATIONS['Peachtree Burger Highland']
SOUTHLAND = settings.LOCATIONS['Peachtree Burger Southland']
MIDTOWN = settings.LOCATIONS['Peachtree Burger Midtown']

'''
Description: This function creates new items in the site catalog associated with the enterpriseId passed to this function. BEWARE: There is no delete to delete an item, you must make it as INACTIVE
Parameters: 
-itemName [ The name of the item that you want to create. NOTICE: Spaces are not allowed]
-version [ Which version of the itemName is this. NOTICE: When updating, you must increase this number]
-shortDescription [ A description of the itemName]
-location [ Which site(location) is this item being added to]
-department [ Which department within the site is this location going to]
-enterpriseId [ The alphanumeric id associated with the location. NOTICE: This was created when the site was created. If unknown use query() within siteMaker] 

Returns: N/A
'''


def createItem(itemName, version, shortDescription, location, department):
    url = 'https://api.ncr.com/catalog/items/%s' % (itemName)
    payload = "{\"version\":%s,\"shortDescription\":{\"values\":[{\"locale\":\"en-US\",\"value\":\"%s\"}]},\"status\":\"INACTIVE\",\"merchandiseCategory\":\"%s\",\"departmentId\":\"%s\"}" % (
        version, shortDescription, location, department)
    r = requests.put(url, payload, auth=(HMACAuth()))
    return r.json()


'''
Description: This function returns the item details of the itemName passed
Parameters: itemName [name of the item you want information about]
Returns: returns the json of the item in question. If no results, returns nothing
'''


def getItem(itemName):
    url = url = 'https://api.ncr.com/catalog/items/%s' % itemName
    r = requests.get(url, auth=(HMACAuth()))
    return r.json()


'''
Description: This function will call the catalog bulk getItem function. It will grab all the items associated with a  particular site/resturant 
Parameters: storeName [The name of the store you wish  to call  all the  items from]
Returns: An array with the names of all the items within the storeName.
'''


def getStoreItems(storeName):
    url = 'https://api.ncr.com/catalog/items?merchandiseCategoryId=%s&itemStatus=ACTIVE' % storeName
    r = requests.get(url, auth=(HMACAuth()))
    tempItems = r.json()
    storeItems = []

    for item in tempItems['pageContent']:
        for nestedItem in item['itemId'].values():
            name = nestedItem
            department = item['departmentId']
            result = {}
            result.update({'name': name, 'department': department})
            storeItems.append(result)

    return storeItems


'''
Description: This function creates a priceItem within the catalog API. The priceItem and item are tied together by the itemCode. I am using itemName as a replacement for itemCode

Parameters:
-itemName [The name that you entered for the item, when you made it (str)]
-itemPriceId [ A unique id for the item. (str)]
-version [ Which version of the itemName is this. NOTICE: When updating, you must increase this number]
-price [How much the item will cost]
-enterpriseId [ The alphanumeric id associated with the location. NOTICE: This was created when the site was created. If unknown use query() within siteMaker] 

Returns: N/A
'''


def createPrice(itemName, itemPriceId, version, price, enterpriseId):
    url = 'https://api.ncr.com/catalog/item-prices/%s/%s' % (
        itemName, itemPriceId)
    payload = "{\"version\":%s,\"price\":%s,\"currency\":\"US Dollar\",\"effectiveDate\":\"2020-07-16T18:22:05.784Z\",\"status\":\"INACTIVE\"}" % (
        version, price)
    r = requests.put(url, payload, auth=(HMACAuth(enterpriseId)))


'''
Description: This function will find the priceItem from the associated itemName
Parameters:
-itemName [The name that you entered for the item, when you made it]
-itemPriceId [The itemPriceId you entered when you created the item]
-enterpriseId [ The alphanumeric id associated with the location. NOTICE: This was created when the site was created. If unknown use query() within siteMaker] 
Returns: A json of the priceItem from the requested itemName
'''


def getPrice(itemName, itemPriceId, enterpriseId):
    url = 'https://api.ncr.com/catalog/item-prices/%s/%s' % (
        itemName, itemPriceId)
    r = requests.get(url, auth=(HMACAuth(enterpriseId)))
    return r.json()


'''
Description: This function will get all the priceItems from the given itemNames
Parameters:
itemIds [A list of itemNames]
-enterpriseId [ The alphanumeric id associated with the location. NOTICE: This was created when the site was created. If unknown use query() within siteMaker] 
Returns: A list of priceItems for the given itemNames
'''


def getAllPrices(itemIds, enterpriseId):
    url = 'https://api.ncr.com/catalog/item-prices/get-multiple'
    itemNames = []

    for i in range(len(itemIds)):
        itemNames.append(itemIds[i]['name'])

    modifiedItems = createJsonString(itemNames)

    payload = "{\"itemIds\":[%s]}" % modifiedItems

    r = requests.post(url, payload, auth=(HMACAuth(enterpriseId)))

    tempPrices = r.json()

    itemsWithPrices = []

    i = 0
    for item in tempPrices['itemPrices']:
        result = {}
        price = item.get('price')
        nested = item.get('priceId')
        name = nested.get('itemCode')
        department = -99

        for collection in itemIds:
            if collection['name'] == name:
                department = collection['department']

        price = addChange(price)
        name = addSpacesInbetweenCaptialLetters(name)
        if isUnique(itemsWithPrices, name):
            result.update({'name': name, 'price': price,
                          'department': department})
            itemsWithPrices.append(result)
            i += 1
        else:
            result.update({'name': name, 'price': price})

    return itemsWithPrices


'''
Description: A helper function to help the front end display the item Names correctly. The API does not currently support spaces in the itemName
Parameters: A string
Returns: The string sepearted on the capitals 
'''


def addSpacesInbetweenCaptialLetters(str1):
    return re.sub(r"(\w)([A-Z])", r"\1 \2", str1)


'''
Description: A helper function to build json strings for the getPriceItems payload.
Parameters: items [A list of itemNames to be turned into a json string]
Returns: a string in the correct format for the getPriceItems payload.
'''


def createJsonString(items):
    String = ""

    for item in items:
        String = String + "{\"itemCode\":\"%s\"}," % item

    String = String.rstrip(',')

    return String


def isUnique(dict_list, item):
    for d in dict_list:
        if d['name'] == item:
            return False
    return True


# TODO: Fix this bug when you pass .01 - 0.9
def addChange(string):
    string = str(string)
    if "." not in string:
        string = string + '.00'
    elif ".0" in string:
        string = string + '0'
    return string

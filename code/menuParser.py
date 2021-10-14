import json


class Menu():
    def __init__(self):
        self.appetizers = []
        self.burgers = []
        self.drinks = []
        self.sides = []
        self.sandwiches = []


def getLinkedGroupContents(linkgroup, data):
    for items in data['linkGroups']:
        if items['id'] == linkgroup:
            return items


def getLinkedGoupContentsIds(toppingsList, data):
    priceList = []
    colNumber = 1
    checkNumber = 0
    for ids in toppingsList['linkedItemReferences']:
        for items in data['linkedItems']:
            if ids['posName'] == items['displayName']:
                price = items['prices'][0]['price']
                priceList.append(
                    {
                        'displayName': items['displayName'],
                        'price': price,
                        'image': items['imageUrls'],
                        'colNumber': colNumber
                    },
                )
                if checkNumber == colNumber * 4 - 1:
                    colNumber += 1
                checkNumber += 1

    return priceList


def menuParsing(data):
    menu = Menu()
    groupToppingsList = ['Sandwich-Toppings']
    itemId = 0

    for item in data['salesItems']:

        uniqueToppingsWithPrices = []
        groupToppingsWithPrices = []
        sharedToppingsWithPrices = []

        if bool(item['linkGroupIds']):

            for linkgroup in item['linkGroupIds']:

                if linkgroup != 'Shared-Toppings' and linkgroup not in groupToppingsList:
                    uniqueToppings = getLinkedGroupContents(linkgroup, data)
                    uniqueToppingsWithPrices = getLinkedGoupContentsIds(
                        uniqueToppings, data)

                elif linkgroup == 'Shared-Toppings':
                    sharedToppings = getLinkedGroupContents(linkgroup, data)
                    sharedToppingsWithPrices = getLinkedGoupContentsIds(
                        sharedToppings, data)

                else:
                    groupToppings = getLinkedGroupContents(linkgroup, data)
                    groupToppingsWithPrices = getLinkedGoupContentsIds(
                        groupToppings, data)

        if len(item['imageUrls']):
            image = item['imageUrls'][0]
        else:
            image = ""

        iteminfo = {'id': itemId,
                    'image': image,
                    'displayName': item['displayName'],
                    'description': item['description'],
                    'price': "${:,.2f}".format(item['currentPrice']),
                    'tags': item['tags'],
                    'quantity': 1,
                    'uniqueToppings': uniqueToppingsWithPrices,
                    'sharedToppings': sharedToppingsWithPrices,
                    'groupToppings': groupToppingsWithPrices}
        itemId += 1

        if iteminfo['tags'][0] == 'appetizers':
            menu.appetizers.append(iteminfo)
        elif iteminfo['tags'][0] == 'burgers':
            menu.burgers.append(iteminfo)
        elif iteminfo['tags'][0] == 'drinks':
            menu.drinks.append(iteminfo)
        elif iteminfo['tags'][0] == 'sides':
            menu.sides.append(iteminfo)
        elif iteminfo['tags'][0] == 'sandwiches':
            menu.sandwiches.append(iteminfo)

    return menu.__dict__

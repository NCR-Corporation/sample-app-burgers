import json
 
file = open('currentMenu.json')
data = json.load(file)
file.close()

def getLinkedGroupContents(linkgroup):
    for items in data['linkGroups']:

        if items['id'] == linkgroup:
            return items

def getLinkedGoupContentsIds(toppingsList):
    priceList = []
    for ids in toppingsList['linkedItemReferences']:
        for items in data['linkedItems']:
            if ids['posName'] == items['displayName']:
                   price = items['prices'][0]['price']
                   priceList.append({'displayName':items['displayName'],'price':price})
    print(priceList)
    return priceList

def menuParsing():
    lunchMenuItems = []
    groupToppingsList = ['Sandwich-Toppings']
    #dinnerMenuItems = []

    lunchID = 0
    dinnerID = 0

    for item in data['salesItems']:

        uniqueToppingsWithPrices = []
        groupToppingsWithPrices = []
        sharedToppingsWithPrices = []
           
        if len(item['linkGroupIds'])!= 0:

            for linkgroup in item['linkGroupIds']:

                if linkgroup != 'Shared-Toppings' and linkgroup not in groupToppingsList:
                    uniqueToppings = getLinkedGroupContents(linkgroup)
                    uniqueToppingsWithPrices = getLinkedGoupContentsIds(uniqueToppings)
                  
                elif linkgroup == 'Shared-Toppings':
                    sharedToppings = getLinkedGroupContents(linkgroup)
                    sharedToppingsWithPrices = getLinkedGoupContentsIds(sharedToppings)
               
                else:
                    groupToppings = getLinkedGroupContents(linkgroup)
                    groupToppingsWithPrices = getLinkedGoupContentsIds(groupToppings)
                              
        iteminfo = {"id":lunchID ,"displayName":item['displayName'],'description':item['description'] , 'price': item['currentPrice'],
                    'tags': item['tags'],'uniqueToppings':uniqueToppingsWithPrices,'sharedToppings':sharedToppingsWithPrices, 'groupToppings':groupToppingsWithPrices}
        lunchID += 1
        lunchMenuItems.append((iteminfo))

    return lunchMenuItems
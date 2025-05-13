import requests
import json
from BurgersUnlimited import settings
from HMACAuth import HMACAuth

HIGHLAND = settings.LOCATIONS['Peachtree Burger Highland']
SOUTHLAND = settings.LOCATIONS['Peachtree Burger Southland']
MIDTOWN = settings.LOCATIONS['Peachtree Burger Midtown']

def doubleQ(dict):
    return (json.dumps(dict))


def createPayload(dict):
    eDict = {}
    quantity = {
        "unitOfMeasure": "EA",
        "unitOfMeasureLabel": "",
        "value": dict['qty'],
    }
    unitPrice = dict["price"]
    productId = {
        "type": "",
        "value": dict['item'],
    }
    eDict.update({"productId": productId})
    eDict.update({"quantity": quantity})
    eDict.update({"unitPrice": unitPrice})

    return eDict


def createOrder(cart):

    results = []

    for dict in range(len(cart)):
        results.append(createPayload(cart[dict]))
    modified_results = doubleQ(results)

    customer = {
        "email": "test@ncr.com",
        "firstName": "Testy",
        "lastName": "McTest Test"
    }

    modified_customer = doubleQ(customer)
    payload = "{\"comments\":\"This is a test4\",\"customer\":%s,\"orderLines\":%s}" % (
        modified_customer, modified_results)
    url = 'https://api.ncr.com/order/orders'
    res = requests.post(url, payload, auth=(
        HMACAuth(settings.LOCATIONS["Burgers Unlimited Southland"])))
    result = res.json()
    return result['id']


def getOrder(orderId):
    headers = {
        'content-type': 'application/json',
        'nep-organization': 'burgers-unlimited',
        'nep-correlation-id': '2020-0708',
    }
    url = 'https://api.ncr.com/order/3/orders/1/%s' % orderId
    res = requests.get(url, auth=(HMACAuth()), headers=headers)
    result = res.json()


cart = [{'item': 'SmallFries', 'price': 9.00, 'qty': 2}, {'item': 'Tunaburger',
                                                          'price': 13.00, 'qty': 2}, {'item': 'milkshake', 'price': 11.00, 'qty': 2}]


def getOrders():
    url = 'https://api.ncr.com/order/3/orders/1/find?pageNumber=0&pageSize=10'

    payload = "{\"customerEmail\":\"test@ncr.com\",\"returnFullOrders\":true}"

    res = requests.post(url, payload, auth=(HMACAuth()))
    result = res.json()

def create_order_from_cart(cart, location):
    if isinstance(cart, str):
        try:
            cart = json.loads(cart)
        except Exception as e:
            raise ValueError(f"Failed to parse cart JSON string: {e}")

    if not isinstance(cart, list):
        raise ValueError(f"Cart must be a list of dicts, got: {type(cart)}")

    order_lines = []
    for item in cart:
        if not all(k in item for k in ['displayName', 'quantity', 'price']):
            raise ValueError(f"Missing required fields in cart item: {item}")

        try:
            price_float = float(item['price'].replace('$', '').strip())
        except:
            raise ValueError(f"Invalid price format: {item['price']}")

        order_lines.append({
            "productId": {
                "type": "",
                "value": item["displayName"]
            },
            "quantity": {
                "unitOfMeasure": "EA",
                "unitOfMeasureLabel": "",
                "value": item["quantity"]
            },
            "unitPrice": price_float
        })

    payload = {
        "channel": "Web",
        "comments": "Created from online checkout",
        "customer": {
            "email": "test@ncr.com",
            "firstName": "Test",
            "lastName": "Demo"
        },
        "orderLines": order_lines
    }

    if location == 'Highland':
        locationId = HIGHLAND
    elif location == 'Midtown':
        locationId = MIDTOWN
    elif location == 'Southland':
        locationId = SOUTHLAND
    else:
        locationId = MIDTOWN

    headers = {
        'nep-organization': 'hospitality-sample-app-dev',
        'nep-enterprise-unit': locationId,
        'nep-service-version': '3:1',
        'content-type': 'application/json',
        'accept': 'application/json',
    }

    if not headers['nep-enterprise-unit']:
        raise ValueError(f"Invalid location or missing enterprise unit for: {location}")

    res = requests.post('https://api.ncr.com/order/orders', json=payload, auth=(HMACAuth(locationId, content_types='application/json')))

    if not res.ok:
        raise Exception(f"Order creation failed: {res.status_code} - {res.text}")

    result = res.json()
    return result.get("id", "unknown")

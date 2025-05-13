import base64
import hashlib
import hmac
from datetime import datetime
from urllib.parse import urlparse

import requests
from _datetime import timezone

from BurgersUnlimited.settings import *


class HMACAuth(requests.auth.AuthBase):

    def __init__(self, enterprise_unit='0', content_types='application/javascript'):
        """
        Constructs all necessary attributes for the HMACAuth object.

        :param enterprise_unit: id of the nep enterprise unit the request applies to
        """
        self.enterprise_unit = enterprise_unit
        self.hmac_shared_key = HMAC_SHARED_KEY
        self.hmac_secret_key = HMAC_SECRET_KEY
        self.organization = NEP_ORGANIZATION
        self.content_types = content_types

    def __call__(self, request):
        """
        Constructs HMAC to uniquely sign a HTTP authorization request.

        :param request: the HTTP request
        :return: the full credentials string for the HTTP Authorization header
        """
        now = datetime.now(tz=timezone.utc)
        now = datetime(now.year, now.month, now.day, hour=now.hour,
                       minute=now.minute, second=now.second)

        isoDate = now.isoformat(timespec='milliseconds') + 'Z'
        utcDate = now.strftime('%a, %d %b %Y %H:%M:%S GMT')

        # Get the one-time key with the current date string
        key = self.customKey(isoDate)

        # Parse date string from header to a native representation
        parsedUrl = urlparse(request.url)

        # Get data from the request headers to sign in the HMAC string
        request.headers['Date'] = utcDate
        request.headers['Content-Type'] = self.content_types

        if self.enterprise_unit != '0':
            request.headers['nep-enterprise-unit'] = self.enterprise_unit

        request.headers['nep-correlation-id'] = '2020-0708'
        request.headers['nep-organization'] = self.organization

        # Add the request data to the sign-able content
        self.addAuthorization(request, key)

        return request

    def customKey(self, date):
        """
        Generates a unique one-time key from the secret key and date string.

        :param date: the date string (ISO-8601 format)
        :return: a unique UTF-8 encoded key
        """
        key = self.hmac_secret_key + date
        return key.encode('utf-8')

    def addAuthorization(self, request, key):
        """
        Generates the HMAC signature for a HTTP authorization request.

        :param request: the HTTP request
        :param key: the access key string
        """
        parsedUrl = urlparse(request.url)
        pathAndQuery = parsedUrl.path
        if parsedUrl.query:
            pathAndQuery += '?' + parsedUrl.query

        # HTTP method and path/query are required parameters
        values = [request.method, pathAndQuery]

        # Add the HTTP header values to the sign-able content
        values.append(request.headers['Content-Type'])

        if 'nep-correlation-id' in request.headers:
            values.append(request.headers['nep-correlation-id'])

        values.append(request.headers['nep-organization'])

        separator = "\n"
        params = separator.join(values)

        # Convert the sign-able content to UTF-8 encoding
        encodedParams = params.encode('utf-8')

        # Calculate the HMAC using the SHA-512 algorithm
        hash = hmac.new(key, encodedParams, hashlib.sha512)
        digest = base64.b64encode(hash.digest()).decode('utf-8')

        # Concatenate the shared key and HMAC strings (UTF-8)
        accessKey = self.hmac_shared_key + ":" + digest

        # Add the signature to the HTTP authorization header
        request.headers['Authorization'] = "AccessKey " + accessKey

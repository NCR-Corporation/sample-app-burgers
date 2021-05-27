# NCR Burgers Unlimited

The NCR Burger Demo serves as an example of how individual APIs in the Business Services Platform (BSP) can be used together to build a functional product.

This repository contains sample code for a fictitious burger restaurant chain to demonstrate how some of NCR's available APIs can be used to facilitate a traditional hospitality ordering experience. It can also be used to understand the HMAC (hash-based message authentication code) algorithm used within BSP.

In future updates, we aim to:

- Visually capture API calls made by the server
- Visually capture errors from any failed requests made to the APIs
- Link together the user registration system and order system
- Implement a customer loyalty system

## Table of Contents

- **[Installation](#installation)**
- **[Setting up the Developer Environment](#setting-up-the-developer-environment)**
- **[Usage](#usage)**
- **[Notes](#notes)**
- **[Troubleshooting](#troubleshooting)**
- **[Contributin](#contributing)**
- **[License](#license)**

## Installation

You will need to have the following:

1. Python 3.0 version or [higher](https://www.python.org/downloads/).
2. A Python IDE, we chose [PyCharm](https://www.jetbrains.com/pycharm/download/#section=mac).
3. Django latest version.
   - Open PyCharm terminal and type `$ python3 -m pip install Django`
4. Python Requests module.
   - Open PyCharm terminal and type `$ python3 -m pip install requests`
5. Django packages. Run the following commands in PyCharm terminal.
   - [Django Compressor](https://django-compressor.readthedocs.io/en/stable/) `$ python3 -m pip install django_compressor`
   - [Django REST framework](https://www.django-rest-framework.org/) `$ python3 -m pip install djangorestframework`
   - [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) `$ python3 -m pip install django-debug-toolbar`
   - [django-requests-debug-toolbar](https://github.com/marceltschoppch/django-requests-debug-toolbar) `$ python3 -m pip install django-requests-debug-toolbar`
   - [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/) `$ python3 -m pip install django-crispy-forms`
   - [django-web-profiler](https://github.com/MicroPyramid/django-web-profiler) `$ python3 -m pip install django-web-profiler`

## Setting up the Developer Environment

Ensure that you have access to your Shared Key, Secret Key, NEP Application Key, and NEP Organization. Inside of the Settings file ( found in _/ncr-burgers-demo/code/BugersUnlimited_), fill in those values with your credentials. Once the values have been filled in, you will need to create your sites and catalog.

1. Creating Sites
   - As part of the initial configuration, you will need to set up at least two sites. Instructions for doing so can be found under [Site documentation](https://developer.ncr.com/portals/dev-portal/api-explorer/details/15/documentation?version=1.99&path=post_sites_import) in the DevEx portal and in the [reference material](https://burgersdemo.ncrcloud.com/burger/about#Sites_Quick_Start) on the application demo site.
2. Creating a Catalog
   - You will also need to set up your catalog at this time. This will serve as your menu. Instructions can be found in the [Catalog documentation](https://developer.ncr.com/portals/dev-portal/api-explorer/details/8/documentation?version=2.99) in the DevEx portal and in the [reference material](https://burgersdemo.ncrcloud.com/burger/about#Tutorial_Catalog) on the application demo site.

Once your developer environment has been installed and configured using the steps above, you will be ready to use the sample app.

## Usage

To run the sample app, enter the following commands from the root directory in Terminal:

```bash
$ cd code
$ pip install -r requirements.txt
$ python3 manage.py migrate
$ python3 manage.py runserver
```

The sample app should open to the main page, where the user can input an address into the search box and choose a search radius (in miles).

- If results are found, the user will be able to select a restaurant.
  - If no results are found, the user will be prompted to return to the home screen.
- If the user selects a restaurant, they will be directed to that restaurant’s menu, where they can add available items to their cart.
  - Once the user has finished adding items to the cart, or if they wish to edit its contents, they can click the “View Cart | Edit Cart” button.
- The user will then be taken to a page where they may update their cart as desired.
- Once satisfied with the contents of their cart, the user can place their order by clicking the “Checkout” button.
- The payment page in the demo is disabled for safety reasons.
- Users should next navigate to the documentation page to learn which APIs were used and how they were implemented in the above processes.

## Notes

The following APIs from the Business Services Platform are used in the NCR Burger Demo app. You can learn more each by clicking on it in the list below.

- [Sites](https://developer.ncr.com/portals/dev-portal/api-explorer/details/645/overview)
- [Catalog](https://developer.ncr.com/portals/dev-portal/api-explorer/details/453/overview)
- [Order](https://developer.ncr.com/portals/dev-portal/api-explorer/details/374/overview)

_Please note that if you don’t set up your sites and catalog, your sample app will not function correctly._

If you are using the sample app to learn more about the Business Services Platform’s HMAC algorithm, you should review the following documentation:

- [Burger Demo reference material](https://burgersdemo.ncrcloud.com/burger/about#Authentication_HMAC)
- [HMACAuth file](code/HMACAuth.py) (in the _/ncr-burger-demo/code_ folder)

## Troubleshooting

If the **Profiler** tab is missing in the application, check the browser inspector for a console error like the one below:

"_Failure to load module script: The server responded with a non JavaScript MIME type..."_

The issue may have been caused by improper content mapping with Django's `runserver` command. For additional troubleshooting information, please reference [this article](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#troubleshooting).

Any other problems? Feel free to open an issue.

## Contributing

Thank you for contributing to this repository to help it become even better.

If you are looking to add a new feature, be sure to create a new issue (either feature or bug) to track the changes. From there, create a PR onto the repository and confirm all workflows run successfully.

## License

This sample app project was released under the [Apache 2.0 license](https://github.com/NCR-Corporation/sample-app-burgers/blob/main/LICENSE).

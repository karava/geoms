from django.shortcuts import HttpResponse
from django.http import JsonResponse
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from apis import constants
from datetime import datetime,timedelta
import pytz
import json


@csrf_exempt
def index(request):
    if request.method == "POST":
        # quoteData = request.POST.copy()
        quoteData = json.loads(request.body)
        customer = quoteData.get("customer")
        print(customer)
    else:
        print("invalid request")
        return HttpResponse("Only POST request permitted")

    # Check if customer already exists
    contactID = checkIfCustomerExists(customer)
    if contactID == False:
        contactID = createNewContact(customerName=customer)
    quoteData["contactID"] = contactID

    # Create new quote
    response = createNewQuote(quoteData=quoteData)
    quoteID = response["Quotes"][0]["QuoteID"]
    quoteNumber = response["Quotes"][0]["QuoteNumber"]

    response = getQuotePDF(quoteID)
    response = HttpResponse(response, content_type='application/pdf')
    filename = f'{quoteID}|{quoteNumber}.pdf'
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

    return response


def fetchXeroAccessToken():
    username = settings.XERO_CLIENT_ID
    password = settings.XERO_CLIENT_SECRET
    headers = {'Content-Type'  : 'application/x-www-form-urlencoded'}
    data = {'grant_type' : 'client_credentials'}

    response = requests.post("https://identity.xero.com/connect/token", headers=headers, data=data, auth=HTTPBasicAuth(username, password))
    response_data = response.json()
    token = response_data["access_token"]
    return token


def checkIfCustomerExists(customerName):
    response = prepareXeroAPICall(apiUrl=f'https://api.xero.com/api.xro/2.0/Contacts?where=Name="{customerName}"', method="GET")
    if response["Contacts"] == []:
        return False
    else:
        return response["Contacts"][0]["ContactID"]


def createNewContact(customerName):
    data = {"Name": customerName}

    response = prepareXeroAPICall(apiUrl="https://api.xero.com/api.xro/2.0/Contacts", method="POST", data=data)
    return response["Contacts"][0]["ContactID"]


def prepareXeroAPICall(apiUrl, method, data=None, PDF=False):

    if PDF:
        contentType = 'application/pdf'
    else:
        contentType = 'application/json'

    XERO_ACCESS_TOKEN = fetchXeroAccessToken()
    headers = {
        'Authorization' : 'Bearer ' + XERO_ACCESS_TOKEN,
        'Accept': contentType
    }

    if method == "GET":
        response = requests.get(apiUrl, headers=headers, json = data)
    elif method == "POST":
        print(data)
        response = requests.post(apiUrl, headers=headers, json = data)

    if response.status_code == 200:
        print("All good")
    elif response.status_code == 401:
        if "TokenExpired" in response.text:
            print("401 error: Token expired")

    if PDF:
        return response.content
    else:
        return response.json()


def createNewQuote(quoteData):
    summary = f"""Commodity: {quoteData["commodity"]}
Pricing: {quoteData["pricing"]}
Shipping details: {quoteData["shippingDetails"]}
Packing Dimensions: {quoteData["packingDimensions"]}
Unloading Details: {quoteData["unloadingDetails"]}
Leadtime: {quoteData["leadTime"]}"""
    
    if quoteData.get('deliveryTerms', None) == "DDP":
        bankDetails = constants.AU_BANK_DETAILS
        taxType = "OUTPUT"
        summary = summary + "\n" + f'Delivery address: {quoteData["deliveryAddress"]}' + "\n" + f'Unloading style: {quoteData["unloadingStyle"]}'
        currencyCode = "AUD"
    else:
        bankDetails = constants.US_BANK_DETAILS
        taxType = "EXEMPTOUTPUT"
        currencyCode = "USD"
    
    summary = summary + "\n" + f'Delivery Disclaimer: {quoteData["deliveryDisclaimer"]}'

    currentDateTime = datetime.now(pytz.timezone('Australia/Victoria'))
    today = str(currentDateTime.year)+"-"+str(currentDateTime.month)+"-"+str(currentDateTime.day)
    expiryDateTime = currentDateTime + timedelta(days=14)
    expiryDate = str(expiryDateTime.year)+"-"+str(expiryDateTime.month)+"-"+(str(expiryDateTime.day))

    if quoteData.get('quoteID', None) != None:
        quoteID = quoteData['quoteID']
        print("This is the quote ID: ", quoteID)
    else:
        quoteID = None

    data = {
        "QuoteID": quoteID,
        "Terms": "Payment Terms: " + quoteData["paymentTerms"] + bankDetails + constants.QUOTE_TERMS,
        "Contact": {
            "ContactID": quoteData["contactID"],
        },
        "LineItems": [
            {
                "Description": quoteData["description"],
                "UnitAmount": quoteData["unitPrice"],
                "Quantity": quoteData["qty"],
                "AccountCode": "200",
                "TaxType" : taxType
            }
        ],
        "Date": today,
        "ExpiryDate": expiryDate,
        "CurrencyCode": currencyCode,
        "Title": quoteData["title"],
        "Summary": summary,
        "Tracking": [],
        "LineAmountTypes": "EXCLUSIVE"
    }

    response = prepareXeroAPICall(apiUrl="https://api.xero.com/api.xro/2.0/Quotes", method="POST", data=data)
    return response


def getQuotePDF(quoteID):
    response = prepareXeroAPICall(apiUrl=f"https://api.xero.com/api.xro/2.0/Quotes/{quoteID}", method="GET", PDF=True)
    return response
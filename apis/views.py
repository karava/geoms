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

    return JsonResponse(response, safe=False)

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


def prepareXeroAPICall(apiUrl, method, data=None):
    XERO_ACCESS_TOKEN = fetchXeroAccessToken()
    headers = {
        'Authorization' : 'Bearer ' + XERO_ACCESS_TOKEN,
        'Accept': 'application/json'
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
    else:
        bankDetails = constants.US_BANK_DETAILS
        taxType = "EXEMPTOUTPUT"

    currentDateTime = datetime.now(pytz.timezone('Australia/Victoria'))
    today = str(currentDateTime.year)+"-"+str(currentDateTime.month)+"-"+str(currentDateTime.day)
    expiryDateTime = currentDateTime + timedelta(days=14)
    expiryDate = str(expiryDateTime.year)+"-"+str(expiryDateTime.month)+"-"+(str(expiryDateTime.day))

    

    data = {
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
        "Title": quoteData["title"],
        "Summary": summary,
        "Tracking": [],
        "LineAmountTypes": "EXCLUSIVE"
    }

    response = prepareXeroAPICall(apiUrl="https://api.xero.com/api.xro/2.0/Quotes", method="POST", data=data)
    return response

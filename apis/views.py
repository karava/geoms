from django.shortcuts import HttpResponse
from django.http import JsonResponse, FileResponse
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from apis import constants
from datetime import datetime, timedelta
import pytz
import json
import io
import os
import fitz

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

@csrf_exempt
def sign_pdf(request):
    print("DEBUG: Entering the sign pdf function")
    if request.method == 'POST':
        # Get the PDF bytes from the request body
        pdf_bytes = request.body

        # Open the input PDF file
        pdf_doc = fitz.open(stream=io.BytesIO(pdf_bytes), filetype='pdf')

        # Load the signature image from the server
        signature_image_filename = 'signature.png'
        signature_image_path = os.path.join(settings.BASE_DIR, 'apis', 'private', 'signatures', signature_image_filename)
        with open(signature_image_path, 'rb') as f:
            image_bytes = f.read()
        
        image = fitz.Pixmap(image_bytes)
        image.shrink(4)

        # Get the first page of the PDF file
        page = pdf_doc[0]

        # Get the size of the image and the page
        image_width, image_height = image.width, image.height
        page_width, page_height = page.mediabox.width, page.mediabox.height

        # Calculate the position of the image in the bottom right corner
        image_offset = 20
        image_x = page_width - image_width - image_offset
        image_y = page_height - image_height - image_offset

        # Add the image to the page
        rect = fitz.Rect(image_x, image_y, page_width - image_offset, page_height - image_offset)
        for page in pdf_doc:
            page.insert_image(rect, pixmap=image)

        # Save the modified PDF to bytes
        output_bytes = pdf_doc.write()
        # pdf_doc.close()  # Close the PDF document to ensure its contents are written to output_bytes

        # Create a response with the modified PDF as a file attachment
        response = HttpResponse(output_bytes, content_type='application/pdf')

        return response

    # If the request method is not POST, return a 405 Method Not Allowed error
    return HttpResponse(status=405)

@csrf_exempt
def relay_trello_webhook(request):
    # Replace with your Google Apps Script Web App URL
    GOOGLE_APPS_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbwShnBheJHJ4CmDDn2_OkaPyCgUc4Ja5nQoR6ogLvp-H3vc_EEZXrSmEg80tSsQkpQtaQ/exec'
    print("DEBUG: Attempting to relay trello webhook to GAS")

    if request.method == 'POST':
        response = requests.post(GOOGLE_APPS_SCRIPT_URL, data=request.body)
        print("DEBUG: Status code received from GAS - ", response.status_code)
        print("DEBUG: Message - ", response.content)

        if response.status_code == 200:
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error"}, status=500)

    elif request.method in ('GET', 'HEAD'):
        return HttpResponse(status=200)

    return JsonResponse({"status": "not allowed"}, status=405)


def get_jaybro_branding_theme_id():
    # Define the Xero API endpoint for branding themes
    branding_themes_endpoint = "https://api.xero.com/api.xro/2.0/BrandingThemes"
    
    # Call your function to get the branding themes from Xero API
    branding_themes = prepareXeroAPICall(branding_themes_endpoint, "GET")

    # Find "Jaybro"
    for theme in branding_themes["BrandingThemes"]:
        if theme["Name"] == "Jaybro":
            return theme["BrandingThemeID"]

    return None


@csrf_exempt
def create_jaybro_invoice(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Retrieve the branding theme ID for "Jaybro"
        branding_theme_id = get_jaybro_branding_theme_id()

        # Update the data with the branding theme ID
        data["BrandingThemeID"] = branding_theme_id

        # Create the invoice on Xero using your Xero API wrapper
        invoice_response = prepareXeroAPICall(
            "https://api.xero.com/api.xro/2.0/Invoices", 
            "POST", 
            data
        )

        # Check if the response includes an 'Invoices' field, which indicates a successful creation
        if 'Invoices' in invoice_response:
            invoice_id = invoice_response['Invoices'][0]['InvoiceID']

            # Get Invoice PDF
            pdf_response = prepareXeroAPICall(
                f"https://api.xero.com/api.xro/2.0/Invoices/{invoice_id}", 
                "GET", 
                PDF=True
            )

            # Send the PDF as a response
            response = FileResponse(io.BytesIO(pdf_response), as_attachment=True, filename='invoice.pdf')
            return response

        else:
            return JsonResponse(invoice_response)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)

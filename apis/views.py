from django.shortcuts import HttpResponse
from django.http import JsonResponse
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings


def index(request):
    XERO_ACCESS_TOKEN = fetchXeroAccessToken()
    headers = {
        'Authorization' : 'Bearer ' + XERO_ACCESS_TOKEN,
        'Accept': 'application/json'
        }
    response = requests.get("https://api.xero.com/api.xro/2.0/Invoices", headers=headers)
    if response.status_code == 200:
        print("All good")
    elif response.status_code == 401:
        if "TokenExpired" in response.text:
            print("401 error: Token expired")
        
    json_response = response.json()
    return JsonResponse(json_response)

def fetchXeroAccessToken():
    username = settings.XERO_CLIENT_ID
    password = settings.XERO_CLIENT_SECRET
    headers = {'Content-Type'  : 'application/x-www-form-urlencoded'}
    data = {'grant_type' : 'client_credentials'}

    response = requests.post("https://identity.xero.com/connect/token", headers=headers, data=data, auth=HTTPBasicAuth(username, password))
    response_data = response.json()
    token = response_data["access_token"]
    return token

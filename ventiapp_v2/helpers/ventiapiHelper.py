import json
import requests
from http import HTTPStatus
from datetime import datetime
from odoo import models, fields, api

URL_BASE = "https://ventiapi.azurewebsites.net/"

def GetToken_VA(email, password):
    method_va = "login"
    url_complete = URL_BASE + method_va
    body = {
        "username": email,
        "password": password,
        "grant_type": "password"
    }

    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    request_va = requests.post(url_complete, body, headers=header)
    if request_va.status_code == HTTPStatus.OK:
        response_va = json.loads(request_va.text)
        return response_va        
    return None
from threading import Timer
from odoo import models, fields, api
from http import HTTPStatus
from datetime import datetime
import requests
import logging


BASE_URL = "https://ventiapi.azurewebsites.net/"
_logger = logging.getLogger(__name__)

def call_api(quantity_available, sku, token):
    def call_it():
        endpoint = "api/stock/updatestock"
        url = BASE_URL + endpoint
        bearer_token = "Bearer " + token

        headers = {
            "Authorization": bearer_token,
            "Content-Type": "application/json"
        }

        body = [{
            "sku": sku,
            "quantity": quantity_available
        }]
        
        response = requests.post(url, json=body, headers=headers)
        if (response.status_code == HTTPStatus.OK):
            _logger.info(f"[{datetime.now()}] Send stock by API to Ventiapp sku: {sku} quant: {quantity_available} status: {response.status_code}")
            # print(sku, quantity_available, response.status_code)
        else:
            _logger.error(f"[{datetime.now()}] Failed send stock sku:{sku} quant:{quantity_available} status:{response.status_code}")
            # print(sku, quantity_available, response.status_code)
    try:
        call_api.t.cancel()
    except (AttributeError):
        pass
    call_api.t = Timer(1, call_it)
    call_api.t.start()


class StockQuantInherit(models.Model):
    _inherit = "stock.quant"

    def write(self, vals):
        res = super(StockQuantInherit, self).write(vals)
        if self.product_id.default_code:
            available = self.quantity - self.reserved_quantity
            cred = self.env['ventiapp.credentials'].search([])
            warehouse_cve = cred.location_id
            warehouse = self.env['stock.warehouse'].search([('id', '=', warehouse_cve.id)])

            if warehouse.lot_stock_id == self.location_id:
                call_api(available, self.product_id.default_code, cred.token)
        return res      

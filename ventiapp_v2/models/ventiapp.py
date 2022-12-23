from datetime import datetime, timedelta
from http import HTTPStatus
import json
import requests
from odoo import models, fields, api
from ..helpers import ventiapiHelper
import logging

_logger = logging.getLogger(__name__)

class Ventiapp(models.Model):
    _name = 'ventiapp.credentials'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(tracking=True)
    password = fields.Char()
    token = fields.Char(tracking=True)
    end_Date = fields.Datetime()
    image = fields.Image(string="Image")
    location_id = fields.Many2one('stock.warehouse', string="Almacen")

    def action_test(self):
        cred_venti = self.search([('name', '=', self.name)])
        if cred_venti != None:
            response_va = ventiapiHelper.GetToken_VA(
                cred_venti.name, cred_venti.password)
            if response_va != None:
                token_va = response_va["access_token"]
                today = datetime.now()
                today = today + timedelta(hours=6)

                obj_update = {
                    'token': token_va,
                    'end_Date': today
                }

                cred_venti.write(obj_update)
                _logger.info(f"[{datetime.now()}] Saved credentials Ventiapp in Odoo")
                # print("Saved credentials Ventiapp in Odoo")

    def credentials_cron(self):
        cred_venti = self.env['ventiapp.credentials'].search([])
        if cred_venti != None:
            today = datetime.now()
            if today > cred_venti.end_Date:
                response_va = ventiapiHelper.GetToken_VA(
                    cred_venti.name, cred_venti.password)
                if response_va != None:
                    token_va = response_va["access_token"]
                    today = datetime.now()
                    today = today + timedelta(hours=6)

                    obj_update = {
                        'token': token_va,
                        'end_Date': today
                    }

                    cred_venti.write(obj_update)
                    _logger.info(f"[{datetime.now()}] Token ventiapp updated")

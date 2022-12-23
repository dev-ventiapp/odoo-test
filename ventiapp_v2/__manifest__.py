# -*- coding: utf-8 -*-
{
    'name': "Ventiapp",

    'summary': "Update Stock",

    'description': "Actualización de stock, Odoo - Ventiapp",

    'author': "Ventiapp ®",
    'website': "https://ventiapp.com/",
    'category': 'Ecommerce',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/credentials_view.xml',
    ],
}
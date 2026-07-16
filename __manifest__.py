# -*- coding: utf-8 -*-
{
    'name': "internship_app",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','purchase','stock','account'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/stock_picking_view_inherit.xml',
        'views/account_move_view_inherit.xml',
        'views/sale_order_view_inherit.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'internship_app/static/src/xml/purchase_dashboard.xml',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}


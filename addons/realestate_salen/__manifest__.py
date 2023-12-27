{
    'name': 'Real Estate',
    'version': '1.0',
    'summary': 'Module for managing real estate sales',
    'description': 'This module helps in managing real estate sales within Odoo.',
    'author': 'Ivaniel Salen',
    'category': 'Sales/Real Estate',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        "views/res_users_views.xml",

        'views/estate_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# -*- coding: utf-8 -*-
{
    'name': "napata_seting",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/collage.xml',
        'views/nationalities.xml',
        'views/program.xml',
        'views/state.xml',
        'views/locals.xml',
        'views/parent.xml',
        'views/job.xml',
        'views/acdimac.xml',
        'views/semester.xml',
        'views/fees_type.xml',
        'views/presentationTyep.xml',

        # menus
        'menus/collage.xml',
        'menus/nationalities.xml',
        'menus/job.xml',
        'menus/address.xml',
        'menus/presentationTyep.xml',
        'menus/acdimac.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

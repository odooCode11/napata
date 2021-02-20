# -*- coding: utf-8 -*-
{
    'name': "napata_presntaion",

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
    'depends': [
                'mail',
                'napata_seting'
                 ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/register_wizard.xml',

        # 'views/chackup.xml',
        # 'views/new_presentation.xml',
        # 'views/old_presentation.xml',
        'views/assistant.xml',
        'views/studyfees.xml',
        'views/presntaionfees.xml',
         'views/admissions.xml',
         'views/management_fees.xml',
         'views/register.xml',
        'data/sequence.xml',
        'data/register_sequence.xml',

        # menus
        # 'menus/presntaion.xml',
        'menus/assistant.xml',
        'menus/register.xml',
        'menus/report.xml',
        'menus/configuration.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

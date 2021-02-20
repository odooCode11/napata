# -*- coding: utf-8 -*-
{
    'name': "animal_production",

    'summary': """
    `   
        """,

    'description': """
        
    """,

    'author': "Aiman, Mergani, Mojahed",
    'category': 'Uncategorized',
    'version': '0.1',
    'sequence': '1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        # 'i18n/ar_AA.po',
        'security/security_view.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'wizard/policy_report_wizard.xml',
        'wizard/confirm_report_wizard_view.xml',
        'wizard/project_report_wizard_view.xml',
        'wizard/order_report_wizard_view.xml',
        'wizard/visit_report_wizard_view.xml',
        'wizard/reject_order_report_wizard.xml',
        'wizard/condition_report_wizard.xml',
        'views/views.xml',
        'views/visit_view.xml',
        'reports/orders_template.xml',
        'reports/order_report.xml',
        'reports/visits_template.xml',
        'reports/visits_report.xml',
        'reports/confirm_template.xml',
        'reports/confirm_reoprt.xml',
        'reports/project_template.xml',
        'reports/project_report.xml',
        'reports/reject_template.xml',
        'reports/recject_report.xml',
        'reports/condition_template.xml',
        'reports/condition_report.xml',
        'reports/policy_template.xml',
        'reports/policy_report.xml',
        # 'reports/report.xml',
    ],
    'images': [],
    'application': True,
}

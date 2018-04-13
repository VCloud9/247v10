# -*- coding: utf-8 -*-

# Part of VCloud9 LLC. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Helpdesk Extension',
    'version': '1.3',
    'category': 'Helpdesk',
    'license': 'Other proprietary',
    'price': 0.0,
    'currency': 'EUR',
    'author': 'VCloud9 LLC.',
    'website': 'https://www.vcloud9.com',
    'summary': 'Helpdesk Extend',
    'description': """
            """,
    'depends':[
        'helpdesk',
        'sale',
        'website_contract',
        'stock',
        'hr_timesheet_sheet',
        'timesheet_grid',
        'purchase',
    ],
    'data' : [
#         'security/helpdesk_team_own_ticket_security.xml',
        'security/sale_price_visible_security.xml',
        'security/ir.model.access.csv',
#         'security/helpdesk.reported.issues.csv',
#         'security/helpdesk.cause.csv',
#         'security/helpdesk.resolution.csv',
#         'security/helpdesk.location.csv',
#         'security/helpdesk.make.csv',
        
        
        'data/helpdesk_reported_issues_data.xml',
        'data/helpdesk_causes_data.xml',
        'data/helpdesk_resolution_data.xml',
        'data/helpdesk_location_data.xml',
        'data/helpdesk_make_data.xml',
        'views/helpdesk_view.xml',
        'views/sale_order_view.xml',
        'views/account_invoice_view.xml',
        'views/sale_subscription_view.xml',
        'views/helpdesk_stage_view.xml',
        'views/reported_issues_view.xml',
        'views/cause_view.xml',
        'views/resolution.xml',
        'views/location_view.xml',
        'views/make_view.xml',
        'views/account_analytic_line.xml',
        'views/helpdesk_team_view.xml',
        'views/sale_view.xml',
        'views/purchase_view.xml',
        'views/helpdesk_extend_report.xml',
        'views/sale_subscription_report.xml'
        ],
    'installable':True,
    'auto_install':False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

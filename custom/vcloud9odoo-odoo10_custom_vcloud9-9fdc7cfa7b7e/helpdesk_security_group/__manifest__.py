# -*- coding: utf-8 -*-

# Part of VCloud9 LLC. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Helpdesk Security Group',
    'version': '1.0',
    'category': 'Helpdesk',
    'license': 'Other proprietary',
    'price': 0.0,
    'currency': 'EUR',
    'author': 'VCloud9 LLC.',
    'website': 'https://www.vcloud9.com',
    'summary': 'Helpdesk Security Group',
    'description': """
            """,
    'depends':[
        'helpdesk_extend',
    ],
    'data' : [
        'security/helpdesk_team_own_ticket_security.xml',
        'security/ir.model.access.csv',
        'views/helpdesk_team_view.xml',
        'views/helpdesk_group_view.xml',
        'views/helpdesk_view.xml',
        'views/helpdesk_extend_report_inherit.xml',
        ],
    'installable':True,
    'auto_install':False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

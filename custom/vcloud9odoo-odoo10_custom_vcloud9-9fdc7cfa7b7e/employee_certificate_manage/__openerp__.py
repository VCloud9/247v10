# -*- coding: utf-8 -*-

# Part of Vcloud9. See LICENSE file for full copyright and licensing details.

{
    'name': 'Employee Certificates',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Manage Employee Certificates',
    'description': """   
    We need to create a Certifications App.
 
Requirements:
 
Fields:
1.       Name of Certificate
2.       Certification Partner (From res.partner)
3.       Certification Date - Date
4.       Description/Requirement  - Text Box for Open text description
6.       Certification Expiration Date -Date
7.       Days to Reminder (?)
 
Employee Form will have a new tab called Certifications and employees certifications are added here.
 
Need to have a notification that will send Employee and Manager an Email 60 and 30 days before expiration. Maybe there should be an option to set the days prior to expiration to send reminder
Prerequisite- If a Certification has
 
I created a very similar app in Studio except for I do not know how to do Reminder…. I was going to just have you add the reminder, but figured it would be best to just start from scratch.
 
Also when you click on a certification, list of certified users shows (similar to attachment) And the Certification should be in a bigger font.
 
Here is a starting list of values
 
Climber 
RF Awareness
CPR
OSHA 10
Man Lift
Anritzu
 
Leave Certification Partners blank for now.
""",
    'author': 'Vcloud',
    'website': 'https://www.vcloud9.com',
    'depends': ['hr'],
    'data': [
             'security/hr_security.xml',
             'security/ir.model.access.csv',
             'data/cert_data.xml',
             'data/cron_data.xml',
             'data/first_days_reminder_template.xml',
             'data/second_days_reminder_templates.xml',
             'views/employee_certificate_view.xml',
             'views/certificate_view.xml',
             'views/hr_view.xml',
             ],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

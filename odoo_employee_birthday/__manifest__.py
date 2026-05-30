{
    'name': 'Employee Birthday Tracker',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Track employee birthdays: Today, 3, 7, 15 days ahead — with monthly chart dashboard',
    'description': """
Employee Birthday Tracker for Odoo 18 (Free / LGPL-3)
======================================================
- OWL-powered dashboard: Today / 3 Days / 7 Days / 15 Days KPI groups
- Click any group card to see the filtered employee list instantly
- Monthly birthday distribution bar chart
- Upcoming 15-day list with color-coded urgency badges
- Minimal dependencies: only requires hr + web
    """,
    'author': 'Randy Nguyen',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['hr', 'web'],
    'data': [
        'views/birthday-dashboard-views.xml',  # actions must exist before menus reference them
        'views/menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'odoo_employee_birthday/static/src/css/birthday-dashboard.css',
            'odoo_employee_birthday/static/src/xml/birthday-dashboard.xml',
            'odoo_employee_birthday/static/src/js/birthday-dashboard.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}

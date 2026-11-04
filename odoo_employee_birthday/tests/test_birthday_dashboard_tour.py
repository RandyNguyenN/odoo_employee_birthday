from datetime import date

from odoo.tests import HttpCase, tagged


@tagged('post_install', '-at_install')
class TestBirthdayDashboardTour(HttpCase):

    def test_view_all_opens_birthday_list(self):
        self.env['hr.employee'].create({'name': 'Birthday Tour Employee', 'birthday': date(1990, 6, 15)})
        action = self.env.ref('odoo_employee_birthday.action_employee_birthday_dashboard')
        self.start_tour(f'/odoo/action-{action.id}', 'odoo_employee_birthday_view_all_tour', login='admin')

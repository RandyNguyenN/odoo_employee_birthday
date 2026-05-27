from datetime import date

from odoo import fields, http
from odoo.http import request


def _days_until_birthday(birthday, today):
    """Days until next birthday occurrence. Handles Feb 29 on non-leap years."""
    try:
        candidate = birthday.replace(year=today.year)
    except ValueError:
        candidate = date(today.year, 2, 28)
    if candidate < today:
        try:
            candidate = birthday.replace(year=today.year + 1)
        except ValueError:
            candidate = date(today.year + 1, 2, 28)
    return (candidate - today).days


class EmployeeBirthdayController(http.Controller):

    @http.route('/odoo_employee_birthday/dashboard_data', type='jsonrpc', auth='user')
    def dashboard_data(self):
        today = fields.Date.today()
        employees = request.env['hr.employee'].search([
            ('active', '=', True),
            ('birthday', '!=', False),
        ])

        groups = {k: [] for k in ('today', 'days3', 'days7', 'days15')}
        monthly_stats = [0] * 12

        for emp in employees:
            monthly_stats[emp.birthday.month - 1] += 1
            days = _days_until_birthday(emp.birthday, today)
            if days == 0:
                groups['today'].append(emp)
            if 1 <= days <= 3:
                groups['days3'].append(emp)
            if 1 <= days <= 7:
                groups['days7'].append(emp)
            if 1 <= days <= 15:
                groups['days15'].append(emp)

        def _fmt(emp):
            return {
                'id': emp.id,
                'name': emp.name,
                'department': emp.department_id.name if emp.department_id else '',
                'days': _days_until_birthday(emp.birthday, today),
                'birthday_display': emp.birthday.strftime('%d/%m'),
            }

        upcoming = sorted(
            [_fmt(e) for e in groups['days15']],
            key=lambda x: x['days'],
        )

        return {
            'today_count':  len(groups['today']),
            'days3_count':  len(groups['days3']),
            'days7_count':  len(groups['days7']),
            'days15_count': len(groups['days15']),
            'today_ids':    [e.id for e in groups['today']],
            'days3_ids':    [e.id for e in groups['days3']],
            'days7_ids':    [e.id for e in groups['days7']],
            'days15_ids':   [e.id for e in groups['days15']],
            'today_list':   [_fmt(e) for e in groups['today']],
            'upcoming':     upcoming[:10],
            'monthly_stats': monthly_stats,
        }

from datetime import date

from odoo import api, fields, models


def _days_until_birthday(birthday, today):
    """Days until next birthday occurrence. Handles Feb 29 on non-leap years."""
    if not birthday:
        return -1
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


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    ebd_days_to_birthday = fields.Integer(
        string='Days to Birthday',
        compute='_compute_ebd_days_to_birthday',
        help='Days remaining until this employee\'s next birthday.',
    )
    ebd_birthday_month = fields.Integer(
        string='Birthday Month',
        compute='_compute_ebd_birthday_month',
        store=True,
        help='Stored month number (1–12) for grouping and searching.',
    )

    @api.depends('birthday')
    def _compute_ebd_days_to_birthday(self):
        today = fields.Date.today()
        for emp in self:
            emp.ebd_days_to_birthday = _days_until_birthday(emp.birthday, today)

    @api.depends('birthday')
    def _compute_ebd_birthday_month(self):
        for emp in self:
            emp.ebd_birthday_month = emp.birthday.month if emp.birthday else 0

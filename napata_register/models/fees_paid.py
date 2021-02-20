
from odoo import models, fields, api
import datetime

class feesPaid(models.Model):
    _name = 'napata.feepaid'
    _inherit = ['mail.thread']
    name = fields.Float(string="installment")
    student_id = fields.Many2one('napata.register', string="Student  ID",
                                 ondelete='cascade')
    paid_date = fields.Date(string="Date")

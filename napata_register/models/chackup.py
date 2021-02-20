import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class napataChackup(models.Model):
    _name = 'napata.chackup'
    _inherit = ['mail.thread']
    # studen name
    name = fields.Char(string="full name")
    first = fields.Char(string="First Name")
    second = fields.Char(string="	Second Name")
    third = fields.Char(string="Third Name")
    last = fields.Char(string="Last Name")
    # presantion
    application_fees = fields.Float(string="Application fees")
    receipt_code = fields.Char(string='Receipt Number ' )
    accept_type = fields.Char(string='Accept Type ' )
    form_number = fields.Integer(string='Form Number ')
    pay_date = fields.Char(string='pay Date')
    user_ids =fields.Char(string="System user ", default=lambda self: self.env.user.name)
    # fees
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'done'),
    ], string='Status', default="draft", readonly=True)

    def action_confirm(self):
        # self.state = "done"
        self.env['napata.new_presentation'].create({
            'name': self.name,
            'first_name': self.first,
            'second_name': self.second,
            'third_name': self.third,
            'forth_name': self.last,
            'type_acceptance': self.accept_type,
            # 'type_acceptance': self.form_number,
            'receipt_code': self.receipt_code,
            'pay_date': self.pay_date,
            'application_fees': self.application_fees,

        })


    # code Serial auto no


from odoo import models, fields, api, exceptions,_
import datetime

class napataAccounting(models.Model):
    _inherit = ['mail.thread']
    _name = 'napata.accounting'
    name = fields.Char(string="full name", compute="get_student_name")
    # studnt  full name
    first = fields.Char(string="First Name")
    second = fields.Char(string="	Second Name")
    third = fields.Char(string="Third Name")
    last = fields.Char(string="Last Name")
    # get student name
    money_type = fields.Selection([
        ('sd', 'Receipt Cash (SDG)'),
        ('us', 'Receipt Cash (USD)'),
        ('bank', 'Bank check'),
        ], string='Method Of Payment')
    # end of name field
    preType2 = fields.Many2one('na.pretyep', string='Presntaion Type',
                             ondelete='cascade',    )   
    presentation_fees = fields.Integer(string=" Presentation Fees"   )
    register_fees = fields.Char(straing='Register Fees')
    Study_fees = fields.Float(string="Study Fees")
    fees = fields.Char(string="Study Fees")
    other_fees = fields.Char(string="Study Fees")
    type_fees = fields.Char(string="Type Fees")




    # fees
    receipt_code=fields.Char(string="Receipt Number"
            , copy=False, readonly=True, index=True, default=lambda self: _('New'))
  

    year = fields.Char(string='Date ',  default=lambda self:datetime.datetime.today().strftime('%Y-%m-%d'))
 
    #
    admission_ids=fields.Char(string="admission Name", default=lambda self : self.env.user.name)

    # 
    def get_student_name(self):
        for re in self:
            re.name = str(re.first) + " " + str(re.second) + " " + str(re.third) + " " + str(re.last)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'done'),
    ], string='Status', default="draft", readonly=True)

    @api.onchange('preType2')
    def _compute_fees(self):
        curr_year = datetime.datetime.now().year
        fees = self.env['napata.presntaionfees'].search([('year', '=', curr_year)])
        if fees:

            for record in fees:
                if record.pretyep == self.preType2:
                    
                    if self.preType2.name=="عام":
                        if record.sudaness:
                                self.presentation_fees = record.sudaness
                    elif self.preType2.name=="شواغر":
                        if record.sudaness:
                                self.presentation_fees = record.sudaness
                    elif self.preType2.name=="وافدين":
                             if record.foreigners:
                                self.presentation_fees = record.foreigners
    @api.model
    def create(self, vals):
        if vals.get('receipt_code', _('New')) == _('New'):
            vals['receipt_code'] = self.env['ir.sequence'].next_by_code('napata_accounting.account_code.sequence') or _('New')
            result = super(napataAccounting, self).create(vals)


        return result

    def send_registration(self):
        # if self.fees:
        #   student_ids = self.env['napata.register'].search([('id', '=', self.fees)])
        #   student_ids.register_fees=self.register_fees
        #   student_ids.firest_pay_date=self.year
        #   student_ids.secand_installment_fees = self.Study_fees
        #   student_ids.secand_pay_date = self.year

        # else:
            print("errer")

    #     print(student_ids.name)
    #     print(self.id)
    #     print("&"*20)
    #     print(self.study_id)

    def action_confirm(self):
            self.state = "done"
            self.env['napata.chackup'].create({
                'name': self.name,
                'first': self.first,
                'second': self.second,
                'third': self.third,
                'last': self.last,
                'accept_type': self.preType2.name,
                'application_fees': self.presentation_fees,
                'pay_date': self.year,
                'receipt_code': self.receipt_code,
               })

    #     for rec in res:
    #         self.env['napata.presentation'].create({
    #             'first_name': self.first,
    #             'second_name': self.second,
    #             'third_name': self.third,
    #             'forth_name': self.last,
    #             'name': self.name,
    #             'preType2': self.preType2,
    #             'fees': self.fees,
    #             'pay_date': self.pay_date,
    #             'prenent_code': self.prenent_code,
    #             'admission_ids': self.admission_ids,

    #         })









        #

        # for rec in self:
        #     rec.state="confirm"
            # self.env['napata.presentation'].create({
            #             'first_name': rec.first,
            #             'second_name': rec.second,
            #             'third_name': rec.third,
            #             'forth_name': rec.last,
            #
            #         })




    def action_done(self):
        for rec in self:
            rec.state = "done"



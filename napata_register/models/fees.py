
from odoo import models, fields, api ,exceptions
import datetime
class napataPresntaion(models.Model):
    _name = 'napata.presntaionfees'
    _inherit = ['mail.thread']

    pretyep = fields.Many2one('na.pretyep', string='PresntaionType',
                             ondelete='cascade', required=True)
    sudaness=fields.Float(string="The Sudanese",required=True)
    foreigners=fields.Float(string="Foreigners",required=True)
    year = fields.Char('Study Year',  default=lambda self: datetime.datetime.now().year)

    # @api.constrains('fees')
    # def _check_something(self):
    #     for record in self:
    #         if record.fees < 100:
    #             raise exceptions.ValidationError("Amount cannot be negative")




# @api.onchange('states_id')
# def get_local(self):
#         get_local_list = []
#         Locals = self.env['reg.locals'].search(
#             [('states_id', '=', self.states_id.id)])
#         if Locals:
#             for rec in Locals:
#                 get_local_list.append(rec.id)
#         return {'domain': {'Local_id': [('id', 'in', get_local_list)]}}





class napataStudy(models.Model):
    _name = 'napata.studyfees'
    _inherit = ['mail.thread']
    program=fields.Many2one("na.program",ondelete="cascade",string="program")
    # study fees
    sudaness_study=fields.Float(string="The Sudanese Fees",required=True)
    foreigners_study=fields.Float(string="Foreigners Fees",required=True)
    # register fees
    sdn_register_fees = fields.Float(string="The Sudanese", required=True)
    foriegn_register_fees = fields.Float(string="Foreigners", required=True)
    # card fees
    card_fees_sudan=fields.Float(string="The Sudanese",required=True)
    card_fees_foring = fields.Float(string="Foreigners", required=True)
    year = fields.Char('Study Year',  default=lambda self: datetime.datetime.now().year)
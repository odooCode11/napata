
from addons.napata_seting.models import fees_type
from odoo import models, fields, api
import datetime

class managementFees(models.Model):
    _name = 'napata.managemanentfees'
    _inherit = ['mail.thread']
    name = fields.Many2one('na.feestype', string="Fees Type ",
                                 ondelete='cascade')
    sudanes=fields.Float(string="The Sudanese",required=True)
    foreig=fields.Float(string="Foreigners",required=True)
    year = fields.Char('Study Year',  default=lambda self: datetime.datetime.now().year)
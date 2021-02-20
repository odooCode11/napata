

from odoo import models, fields, api 


class feesType(models.Model):
    _name = 'na.feestype'
    _description = 'fees Type'
    name = fields.Char(string="Fees Type", required=True)





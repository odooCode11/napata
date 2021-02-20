
from odoo import models, fields, api 
class napataNationalities(models.Model):
    _name = 'na.nationalities'
    _description = 'Nationalities name '
    name = fields.Char(string="Nationalities", required=True,help="Nationalities")



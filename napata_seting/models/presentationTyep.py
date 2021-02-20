
from odoo import models, fields, api

class napatapresntaionTyp(models.Model):
    _name = 'na.pretyep'
    _description = 'presntaionType '
    name = fields.Char(string="PresntaionType", required=True)



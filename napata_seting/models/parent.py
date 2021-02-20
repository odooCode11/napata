
from odoo import models,fields,api
class napataParents(models.Model):
    _name='na.parent'
    _description="relative relation" 
    name=fields.Char(string="parent",required=True)
    




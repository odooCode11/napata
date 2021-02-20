

from odoo import models, fields, api 


class napataUniversity(models.Model):
    _name = 'na.acdemic'
    _description = 'university name '
    name = fields.Char(string="Academic level", required=True)





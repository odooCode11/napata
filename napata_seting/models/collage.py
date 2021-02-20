
from odoo import models, fields, api, exceptions

class napataCollage(models.Model):
    _name = 'na.collage'
    _description = 'collage name '
    name = fields.Char(string="Collage Name", required=True,help="enter Name of Collage")


# def _default_head_branch(self):
#     return self.env['na.collage'].search([('name', '=', 'collage')], limit=1).id
#
#
# head_branch = fields.Many2one('na.collage', string='collage', index=True, ondelete='cascade',
#                               default=_default_head_branch)
#     @api.model
#     def _default_tax_group(self):
#         return self.env['na.collage'].search([], limit=1)
#     collage = fields.Many2one('na.collage', string="collage", default=_default_tax_group, required=True)









from odoo import models, fields, api
import datetime 


class napataAdmissions(models.Model):
    _name = 'napata.admission'
    _inherit = ['mail.thread']
    _description = 'student admissions '
    name = fields.Char(string="full name", compute="get_student_name")
    first=fields.Char(string="First Name")
    second=fields.Char(string="	Second Name")
    third=fields.Char(string="Third Name")
    last=fields.Char(string="Last Name")
    program=fields.Many2one("na.program",ondelete="cascade",string="program")
    preType2=fields.Many2one("na.pretyep",ondelete="cascade",string="Presntaion Type")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'done'),
    ], string='Status', default="draft", readonly=True)
    school_name=fields.Char(string="School Name ")
    studentNumber=fields.Char(string="Form Number" )
    year = fields.Char('Admission Year',  default=lambda self: str(datetime.datetime.now().year -1)
                                                               +" / "+str(datetime.datetime.now().year))

    def get_student_name(self):
        for re in self:
            re.name = str(re.first) + " " + str(re.second) + " " + str(re.third) + " " + str(re.last)
    def action_confirm(self):
        print("%"*30)
        print(self.program.name)


    @api.model
    def create(self, vals):
        res = super(napataAdmissions, self).create(vals)
        self.env['napata.register'].create({
            'name': res.name,
            'first_name': res.first,
            'second_name': res.second,
            'third_name': res.third,
            'forth_name': res.last,
            'form_number': res.studentNumber,
            'school_name': res.school_name,
            'main_desires': res.program.name,
        })
        return res





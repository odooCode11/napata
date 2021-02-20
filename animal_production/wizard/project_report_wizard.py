from odoo import models, fields, api


class ProjectReportWizard(models.TransientModel):
    _name = 'project.report.wizard'
    _description = 'Priject Report'

    PARAMETERS = [
        ('general', 'General'),
        ('period_only', 'Period Only'),
        ('period_state', 'Period & State'),
        ('period_locality', 'Period & Locality'),
        ('period_area', 'Period & Area'),
        ('period_department', 'Period & Department'),
        ('period_applicant', 'Period & Applicant'),

    ]

    state_id = fields.Many2one('states', string='State')
    locality_id = fields.Many2one('localities', string='Locality')
    area_id = fields.Many2one('areas', string='Area')
    department_id = fields.Many2one('departments', string='Department')
    Applicant_id = fields.Many2one('applicant', string='Applicant Name')
    from_date = fields.Date(string="From", default=fields.Date.today())
    to_date = fields.Date(string="To", default=fields.Date.today())
    parameter_id = fields.Selection(PARAMETERS, default='general', string='Select Report Parameters')

    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'params': self.parameter_id,
                'state_id': self.state_id.id,
                'locality_id': self.locality_id.id,
                'area_id': self.area_id.id,
                'department_id': self.department_id.id,
                'Applicant_id': self.Applicant_id.id,
                'state_name': self.state_id.name,
                'locality_name': self.locality_id.name,
                'area_name': self.area_id.name,
                'department_name': self.department_id.name,
                'Applicant_name': self.Applicant_id.name,
                'from_date': fields.Date.from_string(self.from_date),
                'to_date': fields.Date.from_string(self.to_date),
            },
        }

        return self.env.ref('animal_production.project_report').report_action(self, data=data)


class ProjectReport(models.AbstractModel):
    _name = 'report.animal_production.project_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        params = data['form']['params']
        state_id = data['form']['state_id']
        locality_id = data['form']['locality_id']
        area_id = data['form']['area_id']
        department_id = data['form']['department_id']
        Applicant_id = data['form']['Applicant_id']
        state_name = data['form']['state_name']
        locality_name = data['form']['locality_name']
        area_name = data['form']['area_name']
        department_name = data['form']['department_name']
        Applicant_name = data['form']['Applicant_name']
        from_date = data['form']['from_date']
        to_date = data['form']['to_date']
        domain = []

        if params == 'general':
            docs = self.env['projects'].search([])

        elif params == 'period_only':
            domain.append(('Start_date', '>=', from_date))
            domain.append(('end_date', '<=', to_date))

        elif params == 'period_state':
            domain.append(('state_id', '=', state_id))
            domain.append(('Start_date', '>=', from_date))
            domain.append(('end_date', '<=', to_date))

        elif params == 'period_locality':
            domain.append(('locality_id', '=', locality_id))
            domain.append(('Start_date', '>=', from_date))
            domain.append(('end_date', '<=', to_date))

        elif params == 'period_area':
            domain.append(('area_id', '=', area_id))
            domain.append(('Start_date', '>=', from_date))
            domain.append(('end_date', '<=', to_date))

        elif params == 'period_department':
            domain.append(('department_id', '=', department_id))
            domain.append(('Start_date', '>=', from_date))
            domain.append(('end_date', '<=', to_date))

        elif params == 'period_applicant':
            domain.append(('Applicant_id', '=', Applicant_id))
            domain.append(('Start_date', '>=', from_date))
            domain.append(('end_date', '<=', to_date))

        docs = self.env['projects'].search(domain)

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'params': params,
            'state_name': state_name,
            'locality_name': locality_name,
            'area_name': area_name,
            'department_name': department_name,
            'Applicant_name': Applicant_name,
            'from_date': from_date,
            'to_date': to_date,
            'docs': docs,
        }

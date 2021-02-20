from odoo import models, fields, api


class PolicyReportWizard(models.TransientModel):
    _name = 'policy.report.wizard'
    _description = 'policies Report'

    PARAMETERS = [
        ('period_only', 'Period Only'),
        ('period_department', 'Period & Department'),

    ]


    department_id = fields.Many2one('departments', string='Department')

    from_date = fields.Date(string="From", default=fields.Date.today())
    to_date = fields.Date(string="To", default=fields.Date.today())
    parameter_id = fields.Selection(PARAMETERS, default='period_only', string='Select Report Parameters')


    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'params': self.parameter_id,

                'department_id': self.department_id.id,
                'department_name': self.department_id.name,
                'from_date': fields.Date.from_string(self.from_date),
                'to_date': fields.Date.from_string(self.to_date),
            },
        }

        return self.env.ref('animal_production.policies_report').report_action(self, data=data)


class PolicyReport(models.AbstractModel):
    _name = 'report.animal_production.policies_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        params = data['form']['params']

        department_id = data['form']['department_id']

        department_name = data['form']['department_name']
        from_date = data['form']['from_date']
        to_date = data['form']['to_date']
        domain = []

        if params == 'period_only':
            docs = self.env['policies'].search([])


        elif params == 'period_department':
            domain.append(('department_id', '=', department_id))
            domain.append(('f_date', '>=', from_date))
            domain.append(('l_date', '<=', to_date))



        docs = self.env['policies'].search(domain)



        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'params': params,
            'department_name': department_name,
            'from_date': from_date,
            'to_date': to_date,
            'docs': docs,
        }

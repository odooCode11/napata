from odoo import models, fields, api


class RejectReportWizard(models.TransientModel):
    _name = 'reject.report.wizard'
    _description = 'Reject order Report'

    PARAMETERS = [
        ('general', 'General'),
        ('period_only', 'Period Only'),
        ('period_state', 'Period & State'),
        ('period_locality', 'Period & Locality'),
        ('period_area', 'Period & Area'),
        ('period_department', 'Period & Department')
    ]

    state_id = fields.Many2one('states', string='State')
    locality_id = fields.Many2one('localities', string='Locality')
    area_id = fields.Many2one('areas', string='Area')
    department_id = fields.Many2one('departments', string='Department')
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
                'state_name': self.state_id.name,
                'locality_name': self.locality_id.name,
                'area_name': self.area_id.name,
                'department_name': self.department_id.name,
                'from_date': fields.Date.from_string(self.from_date),
                'to_date': fields.Date.from_string(self.to_date),
            },
        }

        return self.env.ref('animal_production.reject_report').report_action(self, data=data)


class RejectReport(models.AbstractModel):
    _name = 'report.animal_production.reject_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        params = data['form']['params']
        state_id = data['form']['state_id']
        locality_id = data['form']['locality_id']
        area_id = data['form']['area_id']
        department_id = data['form']['department_id']
        state_name = data['form']['state_name']
        locality_name = data['form']['locality_name']
        area_name = data['form']['area_name']
        department_name = data['form']['department_name']
        from_date = data['form']['from_date']
        to_date = data['form']['to_date']
        domain = []

        if params == 'general':
            docs = self.env['orders'].search([])

        elif params == 'period_only':
            domain.append(('Order_date', '>=', from_date))
            domain.append(('Order_date', '<=', to_date))
            domain.append(('state', '=', 'reject'))

        elif params == 'period_state':
            domain.append(('state_id', '=', state_id))
            domain.append(('Order_date', '>=', from_date))
            domain.append(('Order_date', '<=', to_date))
            domain.append(('state', '=', 'reject'))

        elif params == 'period_locality':
            domain.append(('locality_id', '=', locality_id))
            domain.append(('Order_date', '>=', from_date))
            domain.append(('Order_date', '<=', to_date))
            domain.append(('state', '=', 'reject'))

        elif params == 'period_area':
            domain.append(('area_id', '=', area_id))
            domain.append(('Order_date', '>=', from_date))
            domain.append(('Order_date', '<=', to_date))
            domain.append(('state', '=', 'reject'))

        elif params == 'period_department':
            domain.append(('department_id', '=', department_id))
            domain.append(('Order_date', '>=', from_date))
            domain.append(('Order_date', '<=', to_date))
            domain.append(('state', '=', 'reject'))

        docs = self.env['orders'].search(domain)

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'params': params,
            'state_name': state_name,
            'locality_name': locality_name,
            'area_name': area_name,
            'department_name': department_name,
            'from_date': from_date,
            'to_date': to_date,
            'docs': docs,
        }

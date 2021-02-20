from odoo import models, fields, api


class VisitReportWizard(models.TransientModel):
    _name = 'visit.report.wizard'
    _description = 'Visits Report'

    PARAMETERS = [
        ('general', 'General'),
        ('period_only', 'Period Only'),
        ('period_state', 'Period & State'),
        ('period_locality', 'Period & Locality'),
        ('period_area', 'Period & Area'),
        ('period_department', 'Period & Department'),
        ('period_visit_type', 'Period & Order & Type'),
    ]

    state_id = fields.Many2one('states', string='State')
    locality_id = fields.Many2one('localities', string='Locality')
    area_id = fields.Many2one('areas', string='Area')
    department_id = fields.Many2one('departments', string='Department')
    visit_type = fields.Selection([('I', 'Initial Visit'),
                                   ('p', 'Permission'),
                                   ('O', 'Re Permission')],
                                  string='Visit Type')
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
                'visit_type': self.visit_type,
                'state_name': self.state_id.name,
                'locality_name': self.locality_id.name,
                'area_name': self.area_id.name,
                'department_name': self.department_id.name,
                'from_date': fields.Date.from_string(self.from_date),
                'to_date': fields.Date.from_string(self.to_date),
            },
        }

        return self.env.ref('animal_production.visit_report').report_action(self, data=data)


class VisitReport(models.AbstractModel):
    _name = 'report.animal_production.visit_template'

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
        visit_type = data['form']['visit_type']
        from_date = data['form']['from_date']
        to_date = data['form']['to_date']
        domain = []

        if params == 'general':
            docs = self.env['visits'].search([])

        elif params == 'period_only':
            domain.append(('visit_date', '>=', from_date))
            domain.append(('visit_date', '<=', to_date))

        elif params == 'period_state':
            domain.append(('state_id', '=', state_id))
            domain.append(('visit_date', '>=', from_date))
            domain.append(('visit_date', '<=', to_date))

        elif params == 'period_locality':
            domain.append(('locality_id', '=', locality_id))
            domain.append(('visit_date', '>=', from_date))
            domain.append(('visit_date', '<=', to_date))

        elif params == 'period_area':
            domain.append(('area_id', '=', area_id))
            domain.append(('visit_date', '>=', from_date))
            domain.append(('visit_date', '<=', to_date))

        elif params == 'period_department':
            domain.append(('department_id', '=', department_id))
            domain.append(('visit_date', '>=', from_date))
            domain.append(('visit_date', '<=', to_date))

        elif params == 'period_visit_type':
            domain.append(('visit_type', '=', visit_type))
            domain.append(('visit_type', '>=', from_date))
            domain.append(('visit_type', '<=', to_date))



        docs = self.env['visits'].search(domain)
        rec = self.env['orders'].search(domain, limit=1)
        state = rec.state_id.name
        locality = rec.locality_id.name
        area = rec.area_id.name

        visit = ''
        if visit_type == 'I':
            visit = 'زيارة مبدئية'
        elif visit_type == 'p':
            visit = 'زيارة تصديق'
        else:
            visit = 'زيارة تجديد تصديق'

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'params': params,
            'state_name': state_name,
            'locality_name': locality_name,
            'area_name': area_name,
            'department_name': department_name,
            'visit': visit,
            'state': state,
            'locality': locality,
            'area': area,
            'from_date': from_date,
            'to_date': to_date,
            'docs': docs,
        }

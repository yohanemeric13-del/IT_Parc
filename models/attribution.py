

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Attribution(models.Model):
    _name = 'gestion.attribution'
    _description = "Historique d'attribution d'materiel"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc, id desc'
    _check_company_auto = True

    equipment_id = fields.Many2one(
        'gestion.materiel',
        string='Materiel',
        required=True,
        ondelete='cascade',
        tracking=True,
        check_company=True,
    )
    company_id = fields.Many2one(related='equipment_id.company_id', store=True, readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employe', required=True, tracking=True)
    department_id = fields.Many2one('hr.department', string='Departement', tracking=True)
    date_start = fields.Date(string='Date de debut', required=True, default=fields.Date.context_today, tracking=True)
    date_end = fields.Date(string='Date de fin', tracking=True)
    reason = fields.Text(string='Motif')
    state = fields.Selection(
        [('active', 'Active'), ('closed', 'Terminee')],
        string='Etat',
        default='active',
        required=True,
        tracking=True,
    )

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        for assignment in self:
            assignment.department_id = assignment.employee_id.department_id

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for assignment in self:
            if assignment.date_end and assignment.date_end < assignment.date_start:
                raise ValidationError(_("La date de fin ne peut pas etre anterieure a la date de debut."))

    @api.model_create_multi
    def create(self, vals_list):
        assignments = super().create(vals_list)
        for assignment in assignments.filtered(lambda item: item.state == 'active'):
            other_assignments = assignment.equipment_id.assignment_ids.filtered(
                lambda item: item.id != assignment.id and item.state == 'active'
            )
            other_assignments.action_close()
            assignment.equipment_id.write({
                'employee_id': assignment.employee_id.id,
                'department_id': assignment.department_id.id,
                'state': 'assigned',
                'assign_date': assignment.date_start,
            })
        return assignments

    def action_close(self):
        today = fields.Date.context_today(self)
        for assignment in self:
            assignment.write({
                'state': 'closed',
                'date_end': assignment.date_end or today,
            })

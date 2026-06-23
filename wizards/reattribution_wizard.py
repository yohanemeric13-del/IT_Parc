

from odoo import fields, models, _
from odoo.exceptions import UserError

class ReattributionWizard(models.TransientModel):
    _name = 'gestion.reattribution.wizard'
    _description = "Assistant de reattribution d'materiel"

    equipment_id = fields.Many2one('gestion.materiel', string='Materiel', required=True)
    current_employee_id = fields.Many2one(related='equipment_id.employee_id', string='Employe actuel', readonly=True)
    current_department_id = fields.Many2one(related='equipment_id.department_id', string='Departement actuel', readonly=True)
    new_employee_id = fields.Many2one('hr.employee', string='Nouvel employe', required=True)
    new_department_id = fields.Many2one('hr.department', string='Nouveau departement')
    date_start = fields.Date(string='Date de reattribution', required=True, default=fields.Date.context_today)
    reason = fields.Text(string='Motif', required=True)

    def action_reassign(self):
        self.ensure_one()
        if self.equipment_id.state == 'retired':
            raise UserError(_("Un materiel retire ne peut pas etre reaffecte."))
        department = self.new_department_id or self.new_employee_id.department_id
        self.equipment_id._close_open_assignments()
        self.env['gestion.attribution'].create({
            'equipment_id': self.equipment_id.id,
            'employee_id': self.new_employee_id.id,
            'department_id': department.id,
            'date_start': self.date_start,
            'reason': self.reason,
        })
        return {'type': 'ir.actions.act_window_close'}

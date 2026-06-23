

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Maintenance(models.Model):
    _name = 'gestion.intervention'
    _description = 'Maintenance parc informatique'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'maintenance.request': 'maintenance_request_id'}
    _order = 'date_start desc, id desc'
    _check_company_auto = True

    maintenance_request_id = fields.Many2one(
        'maintenance.request',
        string='Demande de maintenance',
        required=True,
        ondelete='cascade',
        auto_join=True,
        index=True,
    )
    parc_equipment_id = fields.Many2one(
        'gestion.materiel',
        string='Materiel IT',
        required=True,
        ondelete='restrict',
        tracking=True,
        check_company=True,
    )
    intervention_type = fields.Selection(
        [('corrective', 'Corrective'), ('preventive', 'Preventive')],
        string='Type intervention',
        required=True,
        default='corrective',
        tracking=True,
    )
    date_start = fields.Datetime(string='Debut', required=True, default=fields.Datetime.now, tracking=True)
    date_end = fields.Datetime(string='Fin', tracking=True)
    duration_hours = fields.Float(string='Duree (heures)', compute='_compute_duration_hours', store=True)
    cost = fields.Monetary(string='Cout', currency_field='currency_id', tracking=True)
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    intervention_report = fields.Html(string="Rapport d'intervention")

    @api.depends('date_start', 'date_end')
    def _compute_duration_hours(self):
        for intervention in self:
            if intervention.date_start and intervention.date_end:
                delta = intervention.date_end - intervention.date_start
                intervention.duration_hours = delta.total_seconds() / 3600
            else:
                intervention.duration_hours = 0.0

    @api.onchange('parc_equipment_id')
    def _onchange_parc_equipment_id(self):
        for intervention in self:
            intervention.equipment_id = intervention.parc_equipment_id.maintenance_equipment_id
            intervention.company_id = intervention.parc_equipment_id.company_id

    @api.onchange('intervention_type')
    def _onchange_intervention_type(self):
        for intervention in self:
            intervention.maintenance_type = intervention.intervention_type

    @api.constrains('date_start', 'date_end', 'cost')
    def _check_values(self):
        for intervention in self:
            if intervention.date_end and intervention.date_end < intervention.date_start:
                raise ValidationError(_("La date de fin ne peut pas etre anterieure a la date de debut."))
            if intervention.cost < 0:
                raise ValidationError(_("Le cout d'intervention ne peut pas etre negatif."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            equipment = self.env['gestion.materiel'].browse(vals.get('parc_equipment_id'))
            if equipment:
                vals.setdefault('equipment_id', equipment.maintenance_equipment_id.id)
                vals.setdefault('company_id', equipment.company_id.id)
            vals.setdefault('maintenance_type', vals.get('intervention_type', 'corrective'))
        interventions = super().create(vals_list)
        interventions.mapped('parc_equipment_id').action_set_maintenance()
        return interventions

    def write(self, vals):
        if vals.get('parc_equipment_id'):
            equipment = self.env['gestion.materiel'].browse(vals['parc_equipment_id'])
            vals.setdefault('equipment_id', equipment.maintenance_equipment_id.id)
            vals.setdefault('company_id', equipment.company_id.id)
        if vals.get('intervention_type'):
            vals.setdefault('maintenance_type', vals['intervention_type'])
        return super().write(vals)


from odoo import fields, models, _

class Notification(models.Model):
    _name = 'gestion.alerte'
    _description = 'Notification parc informatique'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_deadline, id desc'
    _check_company_auto = True

    name = fields.Char(string='Objet', required=True, tracking=True)
    alert_type = fields.Selection(
        [('warranty', 'Garantie'), ('contract', 'Accord'), ('maintenance', 'Maintenance'), ('other', 'Autre')],
        string='Type',
        required=True,
        default='warranty',
        tracking=True,
    )
    severity = fields.Selection(
        [('info', 'Information'), ('warning', 'Avertissement'), ('critical', 'Critique')],
        string='Severite',
        default='warning',
        required=True,
        tracking=True,
    )
    equipment_id = fields.Many2one('gestion.materiel', string='Materiel', ondelete='cascade', tracking=True)
    contract_id = fields.Many2one('gestion.accord', string='Accord', ondelete='cascade', tracking=True)
    company_id = fields.Many2one('res.company', string='Societe', default=lambda self: self.env.company, required=True)
    date_deadline = fields.Date(string='Echeance', required=True, tracking=True)
    message = fields.Text(string='Message')
    state = fields.Selection(
        [('open', 'Ouverte'), ('done', 'Traitee'), ('cancelled', 'Annulee')],
        string='Etat',
        default='open',
        required=True,
        tracking=True,
    )

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    @staticmethod
    def _severity_from_days(days_left):
        if days_left < 0:
            return 'critical'
        if days_left <= 15:
            return 'critical'
        if days_left <= 30:
            return 'warning'
        return 'info'

    def _alert_message(self, label, days_left):
        if days_left < 0:
            return _("%s est expire depuis %s jour(s).") % (label, abs(days_left))
        return _("%s expire dans %s jour(s).") % (label, days_left)

    def _create_alert_if_missing(self, vals):
        domain = [
            ('alert_type', '=', vals.get('alert_type')),
            ('state', '=', 'open'),
        ]
        if vals.get('equipment_id'):
            domain.append(('equipment_id', '=', vals['equipment_id']))
        if vals.get('contract_id'):
            domain.append(('contract_id', '=', vals['contract_id']))
        existing = self.search(domain, limit=1)
        return existing or self.create(vals)

    def scan_warranty_alerts(self, delay_days=30):
        today = fields.Date.context_today(self)
        created = self.browse()
        equipments = self.env['gestion.materiel'].search([
            ('warranty_date', '!=', False),
            ('state', '!=', 'retired'),
        ])
        for equipment in equipments:
            days_left = (equipment.warranty_date - today).days
            if days_left <= delay_days:
                created |= self._create_alert_if_missing({
                    'name': _("Garantie - %s") % equipment.display_name,
                    'alert_type': 'warranty',
                    'severity': self._severity_from_days(days_left),
                    'equipment_id': equipment.id,
                    'company_id': equipment.company_id.id,
                    'date_deadline': equipment.warranty_date,
                    'message': self._alert_message(_("La garantie"), days_left),
                })
        return created

    def scan_contract_alerts(self, delay_days=60):
        today = fields.Date.context_today(self)
        created = self.browse()
        contracts = self.env['gestion.accord'].search([
            ('date_end', '!=', False),
            ('state', 'in', ('draft', 'active')),
        ])
        for contract in contracts:
            days_left = (contract.date_end - today).days
            if days_left <= delay_days:
                created |= self._create_alert_if_missing({
                    'name': _("Accord - %s") % contract.name,
                    'alert_type': 'contract',
                    'severity': self._severity_from_days(days_left),
                    'contract_id': contract.id,
                    'company_id': contract.company_id.id,
                    'date_deadline': contract.date_end,
                    'message': self._alert_message(_("Le accord"), days_left),
                })
        return created

    def cron_scan_alerts(self):
        params = self.env['ir.config_parameter'].sudo()
        warranty_delay = int(params.get_param('gestion_parc.warranty_alert_delay_days', default=30))
        contract_delay = int(params.get_param('gestion_parc.contract_alert_delay_days', default=60))
        self.scan_warranty_alerts(warranty_delay)
        self.scan_contract_alerts(contract_delay)
        return True

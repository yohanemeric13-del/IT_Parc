

from odoo import fields, models, _

class ScanNotificationsWizard(models.TransientModel):
    _name = 'gestion.scan.alertes.wizard'
    _description = 'Assistant de scan manuel des alertes'

    warranty_delay_days = fields.Integer(string='Delai garanties (jours)', default=30, required=True)
    contract_delay_days = fields.Integer(string='Delai accords (jours)', default=60, required=True)
    scan_warranties = fields.Boolean(string='Scanner les garanties', default=True)
    scan_contracts = fields.Boolean(string='Scanner les accords', default=True)

    def action_scan(self):
        self.ensure_one()
        alerts = self.env['gestion.alerte']
        created = alerts.browse()
        if self.scan_warranties:
            created |= alerts.scan_warranty_alerts(self.warranty_delay_days)
        if self.scan_contracts:
            created |= alerts.scan_contract_alerts(self.contract_delay_days)
        message = _("%s alerte(s) ouverte(s) apres scan.") % len(created)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Scan des alertes'),
                'message': message,
                'type': 'success',
                'sticky': False,
            },
        }



from odoo import fields, models, _
from odoo.exceptions import ValidationError

class RenouvellementAccordWizard(models.TransientModel):
    _name = 'gestion.renouvellement.accord.wizard'
    _description = 'Assistant de renouvellement de accord'

    contract_id = fields.Many2one('gestion.accord', string='Accord', required=True)
    old_date_end = fields.Date(related='contract_id.date_end', string='Ancienne fin', readonly=True)
    new_date_start = fields.Date(string='Nouveau debut', required=True, default=fields.Date.context_today)
    new_date_end = fields.Date(string='Nouvelle fin', required=True)
    new_amount = fields.Monetary(string='Nouveau montant', currency_field='currency_id')
    currency_id = fields.Many2one(related='contract_id.currency_id', readonly=True)
    note = fields.Text(string='Note de renouvellement')

    def action_renew(self):
        self.ensure_one()
        if self.new_date_end < self.new_date_start:
            raise ValidationError(_("La nouvelle date de fin doit etre posterieure au nouveau debut."))
        values = {
            'date_start': self.new_date_start,
            'date_end': self.new_date_end,
            'state': 'active',
        }
        if self.new_amount:
            values['amount'] = self.new_amount
        if self.note:
            values['notes'] = (self.contract_id.notes or '') + '<p>%s</p>' % self.note
        self.contract_id.write(values)
        self.contract_id.message_post(body=_("Accord renouvele jusqu'au %s.") % self.new_date_end)
        return {'type': 'ir.actions.act_window_close'}

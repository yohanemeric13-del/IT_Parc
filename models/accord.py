

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Accord(models.Model):
    _name = 'gestion.accord'
    _description = 'Accord fournisseur IT'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_end, name'
    _check_company_auto = True

    name = fields.Char(string='Reference accord', required=True, tracking=True)
    contract_type = fields.Selection(
        [('maintenance', 'Maintenance'), ('license', 'Licence'), ('warranty', 'Garantie'), ('other', 'Autre')],
        string='Type',
        required=True,
        default='maintenance',
        tracking=True,
    )
    partner_id = fields.Many2one('res.partner', string='Fournisseur', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Societe', default=lambda self: self.env.company, required=True)
    date_start = fields.Date(string='Debut validite', required=True, tracking=True)
    date_end = fields.Date(string='Fin validite', required=True, tracking=True)
    amount = fields.Monetary(string='Montant', currency_field='currency_id', tracking=True)
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    equipment_ids = fields.Many2many(
        'gestion.materiel',
        'gestion_accord_materiel_rel',
        'contract_id',
        'equipment_id',
        string='Materiels couverts',
    )
    purchase_order_id = fields.Many2one('purchase.order', string='Commande fournisseur')
    invoice_id = fields.Many2one('account.move', string='Facture fournisseur')
    state = fields.Selection(
        [('draft', 'Brouillon'), ('active', 'Actif'), ('expired', 'Expire'), ('closed', 'Cloture')],
        string='Etat',
        default='draft',
        required=True,
        tracking=True,
    )
    days_left = fields.Integer(string='Jours restants', compute='_compute_days_left', store=True)
    is_expired = fields.Boolean(string='Expire', compute='_compute_days_left', store=True)
    alert_ids = fields.One2many('gestion.alerte', 'contract_id', string='Notifications')
    notes = fields.Html(string='Notes')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'La reference accord doit etre unique.'),
    ]

    @api.depends('date_end')
    def _compute_days_left(self):
        today = fields.Date.context_today(self)
        for contract in self:
            contract.days_left = (contract.date_end - today).days if contract.date_end else 0
            contract.is_expired = bool(contract.date_end and contract.days_left < 0)

    @api.constrains('date_start', 'date_end', 'amount')
    def _check_contract_values(self):
        for contract in self:
            if contract.date_end < contract.date_start:
                raise ValidationError(_("La date de fin doit etre posterieure a la date de debut."))
            if contract.amount < 0:
                raise ValidationError(_("Le montant du accord ne peut pas etre negatif."))

    def action_activate(self):
        self.write({'state': 'active'})

    def action_close(self):
        self.write({'state': 'closed'})

    def action_mark_expired(self):
        self.write({'state': 'expired'})

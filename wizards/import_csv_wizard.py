

import base64
import csv
from io import StringIO

from odoo import fields, models, _
from odoo.exceptions import UserError

class ImportCsvWizard(models.TransientModel):
    _name = 'gestion.import.csv.wizard'
    _description = "Assistant d'import CSV d'inventaire"

    file = fields.Binary(string='Fichier CSV', required=True)
    filename = fields.Char(string='Nom du fichier')
    delimiter = fields.Selection([(',', 'Virgule'), (';', 'Point-virgule')], string='Separateur', default=';', required=True)
    result = fields.Text(string="Rapport d'import", readonly=True)

    def action_import(self):
        self.ensure_one()
        if not self.file:
            raise UserError(_("Chargez un fichier CSV."))
        decoded = base64.b64decode(self.file).decode('utf-8-sig')
        reader = csv.DictReader(StringIO(decoded), delimiter=self.delimiter)
        required = {'name', 'serial_no'}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise UserError(_("Colonnes obligatoires manquantes : %s") % ', '.join(sorted(missing)))

        created = 0
        ignored = 0
        errors = []
        for index, row in enumerate(reader, start=2):
            serial = (row.get('serial_no') or '').strip()
            name = (row.get('name') or '').strip()
            if not serial or not name:
                errors.append(_("Ligne %s : nom ou numero de serie manquant.") % index)
                continue
            if self.env['gestion.materiel'].search_count([('serial_no', '=', serial)]):
                ignored += 1
                continue
            try:
                self.env['gestion.materiel'].create({
                    'name': name,
                    'serial_no': serial,
                    'code': (row.get('code') or '').strip() or False,
                    'asset_type': (row.get('asset_type') or 'computer').strip(),
                    'model': (row.get('model') or '').strip(),
                    'location': (row.get('location') or '').strip(),
                    'warranty_date': (row.get('warranty_date') or '').strip() or False,
                })
                created += 1
            except Exception as exc:
                errors.append(_("Ligne %s : %s") % (index, exc))

        self.result = _(
            "Import termine.\nLignes creees : %(created)s\nLignes ignorees : %(ignored)s\nErreurs : %(errors)s"
        ) % {
            'created': created,
            'ignored': ignored,
            'errors': len(errors),
        }
        if errors:
            self.result += "\n\n" + "\n".join(errors)
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

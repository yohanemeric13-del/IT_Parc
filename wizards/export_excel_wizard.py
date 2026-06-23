

import base64
from collections import defaultdict
from io import BytesIO

import xlsxwriter

from odoo import fields, models, _

class ExportExcelWizard(models.TransientModel):
    _name = 'gestion.export.excel.wizard'
    _description = 'Assistant export Excel Gestion Parc'

    export_type = fields.Selection(
        [
            ('inventory', 'Inventaire complet'),
            ('maintenance_costs', 'Couts de maintenance mensuels'),
            ('expiring_contracts', 'Accords expirant dans 60 jours'),
        ],
        string='Export',
        required=True,
        default='inventory',
    )

    def action_export(self):
        self.ensure_one()
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        formats = self._formats(workbook)
        filename = {
            'inventory': 'inventaire_gestion_parc.xlsx',
            'maintenance_costs': 'couts_maintenance_gestion_parc.xlsx',
            'expiring_contracts': 'accords_expirants_gestion_parc.xlsx',
        }[self.export_type]

        if self.export_type == 'inventory':
            self._build_inventory_sheet(workbook, formats)
        elif self.export_type == 'maintenance_costs':
            self._build_maintenance_costs_sheet(workbook, formats)
        else:
            self._build_expiring_contracts_sheet(workbook, formats)

        workbook.close()
        output.seek(0)
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(output.read()),
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self',
        }

    def _formats(self, workbook):
        return {
            'title': workbook.add_format({'bold': True, 'font_size': 14}),
            'header': workbook.add_format({'bold': True, 'bg_color': '#4472C4', 'font_color': '#FFFFFF', 'border': 1}),
            'text': workbook.add_format({'border': 1}),
            'money': workbook.add_format({'border': 1, 'num_format': '#,##0.00'}),
            'date': workbook.add_format({'border': 1, 'num_format': 'yyyy-mm-dd'}),
            'warning': workbook.add_format({'border': 1, 'bg_color': '#FFD966'}),
            'critical': workbook.add_format({'border': 1, 'bg_color': '#FF7070'}),
        }

    def _write_headers(self, sheet, headers, formats):
        for col, header in enumerate(headers):
            sheet.write(0, col, header, formats['header'])
            sheet.set_column(col, col, max(14, len(header) + 2))

    def _build_inventory_sheet(self, workbook, formats):
        sheet = workbook.add_worksheet('Inventaire')
        headers = ['Reference', 'Nom', 'Type', 'Serie', 'Employe', 'Departement', 'Site', 'Etat', 'Garantie', 'Valeur']
        self._write_headers(sheet, headers, formats)
        equipments = self.env['gestion.materiel'].search([], order='code, name')
        for row, equipment in enumerate(equipments, start=1):
            values = [
                equipment.code or '',
                equipment.name or '',
                dict(equipment._fields['asset_type'].selection).get(equipment.asset_type, ''),
                equipment.serial_no or '',
                equipment.employee_id.name or '',
                equipment.department_id.name or '',
                dict(equipment._fields['site'].selection).get(equipment.site, ''),
                dict(equipment._fields['state'].selection).get(equipment.state, ''),
                equipment.warranty_date,
                equipment.purchase_value,
            ]
            for col, value in enumerate(values):
                fmt = formats['money'] if col == 9 else formats['date'] if col == 8 else formats['text']
                sheet.write(row, col, value or '', fmt)

    def _build_maintenance_costs_sheet(self, workbook, formats):
        sheet = workbook.add_worksheet('Couts maintenance')
        headers = ['Materiel', 'Mois', 'Cout total', 'Nombre interventions']
        self._write_headers(sheet, headers, formats)
        grouped = defaultdict(lambda: {'cost': 0, 'count': 0})
        interventions = self.env['gestion.intervention'].search([('date_start', '!=', False)])
        for intervention in interventions:
            month = fields.Date.to_date(intervention.date_start).strftime('%Y-%m')
            key = (intervention.parc_equipment_id.display_name, month)
            grouped[key]['cost'] += intervention.cost
            grouped[key]['count'] += 1
        for row, ((equipment_name, month), values) in enumerate(sorted(grouped.items()), start=1):
            sheet.write(row, 0, equipment_name, formats['text'])
            sheet.write(row, 1, month, formats['text'])
            sheet.write(row, 2, values['cost'], formats['money'])
            sheet.write(row, 3, values['count'], formats['text'])

    def _build_expiring_contracts_sheet(self, workbook, formats):
        sheet = workbook.add_worksheet('Accords 60 jours')
        headers = ['Reference', 'Fournisseur', 'Type', 'Fin validite', 'Jours restants', 'Montant', 'Etat']
        self._write_headers(sheet, headers, formats)
        contracts = self.env['gestion.accord'].search([('days_left', '<=', 60), ('state', 'in', ('draft', 'active'))], order='date_end')
        for row, contract in enumerate(contracts, start=1):
            line_format = formats['critical'] if contract.days_left <= 15 else formats['warning']
            values = [
                contract.name,
                contract.partner_id.name,
                dict(contract._fields['contract_type'].selection).get(contract.contract_type, ''),
                contract.date_end,
                contract.days_left,
                contract.amount,
                dict(contract._fields['state'].selection).get(contract.state, ''),
            ]
            for col, value in enumerate(values):
                fmt = formats['money'] if col == 5 else formats['date'] if col == 3 else line_format
                sheet.write(row, col, value or '', fmt)

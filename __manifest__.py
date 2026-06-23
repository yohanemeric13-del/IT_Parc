{
    'name': 'Gestion Parc',
    'version': '18.0.1.0.0',
    'category': 'IT Management',
    'summary': 'Solution de gestion centralisée du parc informatique',
    'description': """
        Module avancé pour la gestion du parc informatique :
        - Inventaire des équipements et actifs
        - Historique des attributions
        - Suivi des maintenances (préventive et curative)
        - Gestion des accords fournisseurs et alertes
        - Tableau de bord OWL interactif
    """,
    'author': 'IT Solutions',
    'website': 'https://www.itsolutions-example.com',
    'depends': [
        'base', 
        'hr', 
        'stock', 
        'purchase', 
        'account', 
        'maintenance', 
        'mail', 
        'contacts', 
        'web'
    ],
    'data': [
        'security/parc_securite.xml',
        'security/ir.model.access.csv',
        'data/gestion_parc_data.xml',
        'wizards/reattribution_wizard_views.xml',
        'wizards/renouvellement_accord_wizard_views.xml',
        'wizards/scan_alertes_wizard_views.xml',
        'wizards/import_csv_wizard_views.xml',
        'wizards/export_excel_wizard_views.xml',
        'views/materiel_views.xml',
        'views/attribution_views.xml',
        'views/intervention_views.xml',
        'views/accord_views.xml',
        'views/alerte_views.xml',
        'report/gestion_parc_reports.xml',
        'report/gestion_parc_report_templates.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'data/gestion_parc_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'gestion_parc/static/src/js/dashboard.js',
            'gestion_parc/static/src/xml/dashboard.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

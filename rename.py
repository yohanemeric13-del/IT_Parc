import os
import glob
import re

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for old, new in replacements.items():
        new_content = new_content.replace(old, new)
        
    # Remove python comments if it's a python file
    if filepath.endswith('.py'):
        # Keep # -*- coding: utf-8 -*- if we want, but user said remove comments
        new_content = re.sub(r'#.*', '', new_content)
        # Remove empty lines that might be left behind
        new_content = re.sub(r'\n\s*\n', '\n\n', new_content)
        
    # Remove xml comments if it's an xml file
    if filepath.endswith('.xml'):
        new_content = re.sub(r'<!--.*?-->', '', new_content, flags=re.DOTALL)
        new_content = re.sub(r'\n\s*\n', '\n\n', new_content)
        
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

replacements = {
    "'it.equipement'": "'gestion.equipement'",
    '"it.equipement"': '"gestion.equipement"',
    "'it.affectation'": "'gestion.affectation'",
    '"it.affectation"': '"gestion.affectation"',
    "'it.intervention'": "'gestion.intervention'",
    '"it.intervention"': '"gestion.intervention"',
    "'it.contrat'": "'gestion.contrat'",
    '"it.contrat"': '"gestion.contrat"',
    "'it.alerte'": "'gestion.alerte'",
    '"it.alerte"': '"gestion.alerte"',
    
    "'it.reaffectation.wizard'": "'gestion.reaffectation.wizard'",
    '"it.reaffectation.wizard"': '"gestion.reaffectation.wizard"',
    "'it.renouvellement.contrat.wizard'": "'gestion.renouvellement.contrat.wizard'",
    '"it.renouvellement.contrat.wizard"': '"gestion.renouvellement.contrat.wizard"',
    "'it.scan.alertes.wizard'": "'gestion.scan.alertes.wizard'",
    '"it.scan.alertes.wizard"': '"gestion.scan.alertes.wizard"',
    "'it.import.csv.wizard'": "'gestion.import.csv.wizard'",
    '"it.import.csv.wizard"': '"gestion.import.csv.wizard"',
    "'it.export.excel.wizard'": "'gestion.export.excel.wizard'",
    '"it.export.excel.wizard"': '"gestion.export.excel.wizard"',

    "it.equipement": "gestion.equipement",
    "it.affectation": "gestion.affectation",
    "it.intervention": "gestion.intervention",
    "it.contrat": "gestion.contrat",
    "it.alerte": "gestion.alerte",
    "it.reaffectation.wizard": "gestion.reaffectation.wizard",
    "it.renouvellement.contrat.wizard": "gestion.renouvellement.contrat.wizard",
    "it.scan.alertes.wizard": "gestion.scan.alertes.wizard",
    "it.import.csv.wizard": "gestion.import.csv.wizard",
    "it.export.excel.wizard": "gestion.export.excel.wizard",
    
    "IT Parc": "Gestion Parc",
    "TECHPARK CI": "IT Solutions",
    "https://www.techpark.ci": "https://www.itsolutions-example.com",
    
    "ItEquipement": "Materiel",
    "ItAffectation": "Attribution",
    "ItIntervention": "Maintenance",
    "ItContrat": "Accord",
    "ItAlerte": "Notification",
    "ItAccord": "Accord",
    "ItMateriel": "Materiel",
    "ItAttribution": "Attribution",
    "ItNotification": "Notification",
    "ItMaintenance": "Maintenance",
    "ItReattributionWizard": "ReattributionWizard",
    "ItRenouvellementContratWizard": "RenouvellementContratWizard",
    "ItRenouvellementAccordWizard": "RenouvellementAccordWizard",
    "ItScanAlertesWizard": "ScanAlertesWizard",
    "ItScanNotificationsWizard": "ScanNotificationsWizard",
    "ItImportCsvWizard": "ImportCsvWizard",
    "ItExportExcelWizard": "ExportExcelWizard",
    
    "it_accord_materiel_rel": "gestion_accord_materiel_rel",
    "it_parc.": "gestion_parc.",
    "it_parc/": "gestion_parc/",
    "it_parc_": "gestion_parc_",

    "model_it_alerte": "model_gestion_alerte",
    "model_it_equipement": "model_gestion_equipement",
    "model_it_affectation": "model_gestion_affectation",
    "model_it_intervention": "model_gestion_intervention",
    "model_it_contrat": "model_gestion_contrat",
    "model_it_accord": "model_gestion_accord",
    "model_it_materiel": "model_gestion_materiel",
    "model_it_attribution": "model_gestion_attribution",
    
    "IT-PC-": "GP-PC-",
    "IT-SRV-": "GP-SRV-",
    "IT-PRN-": "GP-PRN-",
    "IT-NET-": "GP-NET-",
    "IT-TEL-": "GP-TEL-",
    "IT-LIC-": "GP-LIC-",
    "IT-UPS-": "GP-UPS-",
    "IT-SCAN-": "GP-SCAN-",
    
    "employee_demo_it_": "employee_demo_gp_",
    "partner_demo_it_": "partner_demo_gp_",
    
    "Équipements": "Matériels",
    "Équipement": "Matériel",
    "equipement": "materiel",
    "Equipement": "Materiel",
    
    "Affectations": "Attributions",
    "Affectation": "Attribution",
    "affectation": "attribution",
    
    "Contrats": "Accords",
    "Contrat": "Accord",
    "contrat": "accord",
    
    "Alertes": "Notifications",
    "Alerte": "Notification",
    
    "Interventions": "Maintenances",
    "Intervention": "Maintenance",
    
    "view_it_equipement": "view_gestion_equipement",
    "view_it_affectation": "view_gestion_affectation",
    "view_it_intervention": "view_gestion_intervention",
    "view_it_contrat": "view_gestion_contrat",
    "view_it_alerte": "view_gestion_alerte",
    
    "action_it_equipement": "action_gestion_equipement",
    "action_it_affectation": "action_gestion_affectation",
    "action_it_intervention": "action_gestion_intervention",
    "action_it_contrat": "action_gestion_contrat",
    "action_it_alerte": "action_gestion_alerte",
}

def main():
    base_dir = r"D:\Marc-aurel\IT_Parc"
    extensions = ["*.py", "*.xml", "*.csv", "*.js"]
    
    files_to_process = []
    for ext in extensions:
        files_to_process.extend(glob.glob(os.path.join(base_dir, "**", ext), recursive=True))
        
    for filepath in files_to_process:
        if "rename.py" in filepath or "__pycache__" in filepath:
            continue
        replace_in_file(filepath, replacements)
        
if __name__ == "__main__":
    main()

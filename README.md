# Gestion Parc

**Gestion Parc** est un module Odoo puissant et intuitif conçu pour centraliser et optimiser le suivi du matériel informatique au sein de votre organisation.

##  Fonctionnalités Principales

- **Inventaire Détaillé des Matériels** : Maintenez une liste complète de tous vos actifs informatiques (ordinateurs, serveurs, licences, équipements réseau) avec des fiches détaillées (numéros de série, types, dates d'achat, garanties).
- **Historique des Attributions** : Suivez qui possède quel matériel. Gardez une trace chronologique complète de toutes les dotations et restitutions effectuées par vos collaborateurs.
- **Gestion des Maintenances** : Planifiez et suivez toutes les opérations de maintenance (préventive et curative) pour réduire les temps d'arrêt.
- **Suivi des Accords Fournisseurs** : Gérez vos contrats d'assistance et de garantie. Recevez des notifications automatiques avant leur expiration.
- **Tableau de Bord Dynamique** : Profitez d'une vue d'ensemble grâce à un tableau de bord (développé en OWL) permettant d'analyser vos coûts de maintenance et l'état de votre parc en temps réel.
- **Import/Export de Données** : Intégrez facilement des données existantes ou générez des rapports Excel via des assistants (wizards) dédiés.

##  Installation

1. Téléchargez ou clonez le dossier `it_parc` dans le répertoire des addons de votre instance Odoo.
2. Assurez-vous d'avoir les dépendances requises (modules de base tels que `hr`, `maintenance`, `stock`, `purchase`).
3. Redémarrez le service Odoo.
4. Activez le mode développeur, mettez à jour la liste des applications.
5. Recherchez **Gestion Parc** et cliquez sur *Installer*.

##  Guide d'Utilisation Rapide

1. **Création d'un Matériel** : Allez dans *Gestion Parc > Matériels* et créez un nouvel enregistrement pour votre actif.
2. **Attribution** : Depuis la fiche du matériel, cliquez sur le bouton d'attribution pour assigner le matériel à un employé.
3. **Planification de Maintenance** : Créez une nouvelle intervention liée à un matériel défectueux depuis le menu *Maintenances*.
4. **Configuration d'Accords** : Enregistrez vos contrats d'assurance ou de licence sous *Accords* et associez-les aux matériels concernés.

##  Sécurité & Droits d'Accès

Le module intègre des groupes de sécurité prédéfinis :

- **Manager (Gestionnaire)** : Accès complet (Création, Modification, Suppression) sur tous les objets du module.
- **Technicien** : Accès en lecture sur l'inventaire, avec possibilité de créer et mettre à jour des interventions.

##  Aspect Technique

Ce module exploite plusieurs fonctionnalités avancées d'Odoo :

- **Framework OWL** pour la création de composants interactifs dans le tableau de bord.
- **Héritage** (`_inherits`) pour lier nos matériels informatiques au module de maintenance standard d'Odoo.
- **Actions Planifiées (Cron)** pour le scan automatique des alertes et des accords expirés.

##  Contribution

Les contributions sont toujours les bienvenues ! 
N'hésitez pas à soumettre une pull request ou ouvrir une issue pour proposer des améliorations.

# Changelog — sf_kyc_aml

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- KYC files per partner with risk rating
- PEP/sanctions screening tracking
- UBO declaration and document checklist
- Periodic review cycles with overdue flags
- Expiry workflow and multi-company isolation

### Technique
- Modèles : sf.kyc.file
- Dépendances : base, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés

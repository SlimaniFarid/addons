# Changelog — sf_telecom_expense

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Telecom lines with employees and plan costs
- Contract end tracking with alerts
- Monthly invoice audits per provider
- Expected vs invoiced variance with tolerance
- Multi-company isolation

### Technique
- Modèles : sf.telecom.line, sf.telecom.audit
- Dépendances : base, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés

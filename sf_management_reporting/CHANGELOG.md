# Changelog — sf_management_reporting

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Monthly packs with revenue, costs, margin
- Previous month comparison with delta %
- Custom KPI lines with comments
- Executive commentary section
- Finalize workflow

### Technique
- Modèles : sf.mgmt.report, sf.mgmt.report.kpi
- Dépendances : base, account, sale, purchase, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés

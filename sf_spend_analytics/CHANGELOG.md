# Changelog — sf_spend_analytics

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Spend analysis runs per period
- Vendor and category spend from posted bills
- PO coverage split (covered vs maverick)
- Maverick % with tolerance alerts
- Multi-company isolation

### Technique
- Modèles : sf.spend.analysis, sf.spend.line
- Dépendances : base, account, purchase, product, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés

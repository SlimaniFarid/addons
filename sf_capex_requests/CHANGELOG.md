# Changelog — sf_capex_requests

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- CAPEX requests with categories and business case
- Multi-level approval chain with comments
- Payback computation from annual benefit
- Ordered / Capitalized lifecycle with PO and asset references
- Kanban pipeline and pivot analysis

### Technique
- Modèles : sf.capex.request, sf.capex.approval
- Dépendances : base, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés

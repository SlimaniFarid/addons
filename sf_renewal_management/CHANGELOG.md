# Changelog — sf_renewal_management

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Customer contracts with types, terms, notice periods
- Notice deadline and expiry countdowns
- Churn risk rating and next actions
- Renewed/lost/expired outcomes
- Kanban pipeline and pivot analysis

### Technique
- Modèles : sf.renewal.contract
- Dépendances : base, sale, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés

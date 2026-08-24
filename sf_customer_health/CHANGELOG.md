# Changelog — sf_customer_health

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Health records per customer with owner
- 12-month revenue and trend computation
- Order recency and overdue signals
- Weighted health score with risk ratings
- Kanban board by risk level

### Technique
- Modèles : sf.customer.health
- Dépendances : base, sale, account, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés

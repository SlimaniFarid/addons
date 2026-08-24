# Changelog — sf_inventory_aging

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Aging analysis per warehouse and as-of date
- Days since last movement per product/lot
- 4 aging buckets with configurable provision %
- Provision amount computation
- Multi-company isolation

### Technique
- Modèles : sf.aging.analysis, sf.aging.line
- Dépendances : base, stock, product, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés

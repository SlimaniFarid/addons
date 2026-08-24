# Changelog — sf_price_change_mgmt

## [18.0.1.0.0] / [19.0.1.0.0] — Version initiale

### Fonctionnalités
- Price change campaigns with reasons
- Product lines with old/new prices and delta %
- Effective-date gated application
- One-click price update
- Multi-company isolation

### Technique
- Modèles : sf.price.change, sf.price.change.line
- Dépendances : base, product, sale, mail
- Vues : list, form (+ kanban/pivot selon module)
- Sécurité : groupes User/Manager, règles multi-sociétés
